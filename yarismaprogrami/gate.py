import asyncio
import aiohttp
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from typing import List, Dict, Any, Optional
from contextlib import asynccontextmanager
import redis.asyncio as redis
import json
import uuid

GEMINI_API_KEY = "AIzaSyD9EGmWuDExT5rMyuJeUDbj1-RUPCOI91k"
REDIS_URL = "rediss://default:ASZeAAIjcDE0NjliYmJkYjcwYmI0N2ZlOWQ0ZGI4ZmY1NTFmN2Q4NnAxMA@pet-goose-9822.upstash.io:6379"

ROUTER_URL = "http://127.0.0.1:8001/create_plan"
RETRIEVER_URL = "http://127.0.0.1:8000"
RERANKER_URL = "http://127.0.0.1:8002/rerank"

PROMPT_ANALYZE_FULL_CONTENT = """
SENARYO: Sana, bir kullanıcının sorusunu cevaplamak için web'den toplanmış en alakalı sayfaların tam metin içerikleri ve önceki konuşma geçmişi verildi. Sen, bu detaylı içerikleri ve geçmişi analiz ederek, veriye dayalı, bağlama uygun ve eksiksiz bir cevap hazırlayan uzman bir araştırma analistisin.

{history_context}

KULLANICININ ŞİMDİKİ SORUSU: "{user_query}"
--- SANA SUNULAN TAM SAYFA İÇERİKLERİ (Numaralandırılmış) ---
{context}
--- İÇERİKLERİN SONU ---
GÖREVİN: Yukarıdaki tam sayfa içeriklerini ve konuşma geçmişini kullanarak kullanıcının şimdiki sorusunu en iyi ve en eksiksiz şekilde cevaplayan, kapsamlı ve yapılandırılmış bir metin oluştur. Cevabını SADECE sana sunulan verilere dayandır.
KURALLAR:
1. Eğer bir üniversite veya bölüm listesi sunuyorsan, bunu MUTLAKA Markdown tablosu formatında oluştur.
2. Cevabının en sonuna, "---" ile ayırarak, "Kaynaklar" başlığı altında kullandığın kaynakların tam URL listesini numaralandırarak ekle.
"""
PROMPT_DIRECT_CHAT = """
Sen empatik bir tercih danışmanısın. Adın 'Rehber Asistan'. Kullanıcının önceki konuşmalarını da dikkate alarak şu anki mesaja uygun bir cevap ver.

{history_context}

Kullanıcının Şimdiki Mesajı: "{user_query}"
"""

redis_client = None

class AskRequest(BaseModel):
    query: str
    session_id: Optional[str] = None

def format_history_for_prompt(history: List[Dict[str, str]]) -> str:
    if not history:
        return "Daha önce bir konuşma yapılmadı."
    
    formatted_lines = ["--- ÖNCEKİ KONUŞMA GEÇMİŞİ ---"]
    for msg in history:
        if msg['role'] == 'user' and history.index(msg) == len(history) -1:
            continue
        role = "Siz" if msg['role'] == 'user' else "Rehber Asistan"
        formatted_lines.append(f"{role}: {msg['content']}")
    formatted_lines.append("--- KONUŞMA GEÇMİŞİNİN SONU ---")
    return "\n".join(formatted_lines)

async def call_gemini_synthesis(prompt: str, model_name: str = "gemini-1.5-flash-latest"):
    try:
        model = genai.GenerativeModel(model_name, safety_settings=DEFAULT_SAFETY_SETTINGS)
        response = await model.generate_content_async(prompt, generation_config={"temperature": 0.2})
        return response.text
    except Exception as e:
        print(f"!! [GATEWAY] Gemini Sentezleme Hatasi: {e}")
        return "Üzgünüm, bilgileri sentezlerken bir sorunla karşılaştım."

@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis_client
    print("[GATEWAY] Servis basliyor, Redis'e baglaniliyor...")
    try:
        redis_client = redis.from_url(REDIS_URL, decode_responses=True)
        await redis_client.ping()
        print("[GATEWAY] [OK] Hafiza icin Redis baglantisi kuruldu.")
    except Exception as e:
        print(f"[GATEWAY] [HATA] Redis baglantisi kurulamadi: {e}")
        redis_client = None
    yield
    if redis_client:
        await redis_client.close()
        print("[GATEWAY] Redis bağlantısı kapatıldı.")

app = FastAPI(title="Redis-Powered RAG Gateway", lifespan=lifespan)
genai.configure(api_key=GEMINI_API_KEY)
DEFAULT_SAFETY_SETTINGS = { HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE, }

@app.post("/ask_intelligent")
async def ask_intelligent_system(request: AskRequest):
    if not redis_client:
        return HTTPException(status_code=503, detail="Hafıza servisi (Redis) şu an kullanılamıyor.")

    session_id = request.session_id or str(uuid.uuid4())
    print(f"\n[GATEWAY] Gelen Sorgu | Session ID: {session_id}")

    try:
        history_json = await redis_client.get(f"session:{session_id}")
        conversation_history = json.loads(history_json) if history_json else []
    except Exception as e:
        print(f"[GATEWAY] [HATA] Redis'ten geçmiş okunamadı: {e}")
        conversation_history = []
    
    conversation_history.append({"role": "user", "content": request.query})
    history_for_prompt = format_history_for_prompt(conversation_history)
    original_query = request.query
    final_answer = "Beklenmedik bir hata oluştu."
    sources_used = []
    timeout = aiohttp.ClientTimeout(total=180)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.post(ROUTER_URL, json={"user_query": original_query}) as resp:
                resp.raise_for_status()
                plan = await resp.json()
        except aiohttp.ClientError as e:
            return {"answer": f"Yönlendirici servisine bağlanırken hata oluştu: {e}", "sources_used": [], "session_id": session_id}

        action_type = plan.get("action_type")
        print(f"[GATEWAY] Yönlendirici Kararı: Eylem={action_type}")

        if action_type == "DIRECT_CHAT":
            chat_prompt = PROMPT_DIRECT_CHAT.format(user_query=original_query, history_context=history_for_prompt)
            final_answer = await call_gemini_synthesis(chat_prompt)

        elif action_type == "RAG_SEARCH":
            retriever_payload = { "original_query": original_query, "optimized_queries": plan.get("optimized_queries", []), "extracted_entities": plan.get("extracted_entities", []) }
            async with session.post(f"{RETRIEVER_URL}/retrieve", json=retriever_payload) as resp:
                if resp.status != 200: return {"answer": f"Retriever servisi hata verdi: {await resp.text()}", "sources_used": [], "session_id": session_id}
                doc_snippets = (await resp.json()).get("data", [])
            
            if not doc_snippets:
                final_answer = "İnternet aramalarımda konuyla ilgili bir içerik bulamadım."
            else:
                async with session.post(RERANKER_URL, json={"original_query": original_query, "documents": doc_snippets}) as resp:
                    if resp.status != 200: return {"answer": f"Re-ranker servisi hata verdi: {await resp.text()}", "sources_used": [], "session_id": session_id}
                    ranked_snippets = (await resp.json()).get("ranked_documents", [])

                if not ranked_snippets:
                    final_answer = "Bulunan bilgiler sorunuzla yeterince alakalı görünmüyor."
                else:
                    urls_to_fetch = [doc['document']['url'] for doc in ranked_snippets[:3]]
                    print(f"[GATEWAY] En iyi {len(urls_to_fetch)} kaynağın tam içeriği çekiliyor...")
                    async with session.post(f"{RETRIEVER_URL}/fetch_content", json={"urls": urls_to_fetch}) as resp:
                        if resp.status != 200: return {"answer": f"Detaylı içerik çekilemedi: {await resp.text()}", "sources_used": [], "session_id": session_id}
                        full_content_docs = (await resp.json()).get("data", [])

                    context_parts = [f"--- KAYNAK [{i+1}]: {doc.get('url')} ---\n{doc.get('content')}" for i, doc in enumerate(full_content_docs) if doc.get('content')]
                    if not context_parts:
                        final_answer = "İlgili dökümanların içeriği anlamlı bir şekilde işlenemedi."
                    else:
                        sources_used = [doc.get('url') for doc in full_content_docs if doc.get('content')]
                        detailed_prompt = PROMPT_ANALYZE_FULL_CONTENT.format(user_query=original_query, context="\n\n".join(context_parts), history_context=history_for_prompt)
                        final_answer = await call_gemini_synthesis(detailed_prompt)
                        print("[GATEWAY] Detaylı cevap üretildi. İşlem tamamlandı.")
        else:
            final_answer = "Beklenmedik bir eylem tipi ile karşılaşıldı."

    conversation_history.append({"role": "model", "content": final_answer})

    try:
        if len(conversation_history) > 10:
            conversation_history = conversation_history[-10:]

        await redis_client.set(f"session:{session_id}", json.dumps(conversation_history), ex=86400)
        print(f"[GATEWAY] Oturum hafızası Redis'e güncellendi. (Geçerlilik: 24 saat)")
    except Exception as e:
        print(f"[GATEWAY] [HATA] Redis'e geçmiş yazılamadı: {e}")

    return {"answer": final_answer, "sources_used": sources_used, "session_id": session_id}