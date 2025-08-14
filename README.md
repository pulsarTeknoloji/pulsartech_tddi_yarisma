<div id="top">

<!-- HEADER STYLE: CLASSIC -->
<div align="center">


# PULSAR TECH - TDDİ YARIŞMA

<!-- BADGES -->
<img src="https://img.shields.io/github/last-commit/iamfurkann/nlp-deneme?style=flat&logo=git&logoColor=white&color=0080ff" alt="last-commit">
<img src="https://img.shields.io/github/languages/top/iamfurkann/nlp-deneme?style=flat&color=0080ff" alt="repo-top-language">
<img src="https://img.shields.io/github/languages/count/iamfurkann/nlp-deneme?style=flat&color=0080ff" alt="repo-language-count">

<em>Kullanılar teknolojiler ve araçlar</em>

<img src="https://img.shields.io/badge/Markdown-000000.svg?style=flat&logo=Markdown&logoColor=white" alt="Markdown">
<img src="https://img.shields.io/badge/Redis-FF4438.svg?style=flat&logo=Redis&logoColor=white" alt="Redis">
<img src="https://img.shields.io/badge/scikitlearn-F7931E.svg?style=flat&logo=scikit-learn&logoColor=white" alt="scikitlearn">
<img src="https://img.shields.io/badge/tqdm-FFC107.svg?style=flat&logo=tqdm&logoColor=black" alt="tqdm">
<img src="https://img.shields.io/badge/Babel-F9DC3E.svg?style=flat&logo=Babel&logoColor=black" alt="Babel">
<img src="https://img.shields.io/badge/SymPy-3B5526.svg?style=flat&logo=SymPy&logoColor=white" alt="SymPy">
<img src="https://img.shields.io/badge/Selenium-43B02A.svg?style=flat&logo=Selenium&logoColor=white" alt="Selenium">
<img src="https://img.shields.io/badge/Django-092E20.svg?style=flat&logo=Django&logoColor=white" alt="Django">
<img src="https://img.shields.io/badge/FastAPI-009688.svg?style=flat&logo=FastAPI&logoColor=white" alt="FastAPI">
<br>
<img src="https://img.shields.io/badge/NumPy-013243.svg?style=flat&logo=NumPy&logoColor=white" alt="NumPy">
<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/AIOHTTP-2C5BB4.svg?style=flat&logo=AIOHTTP&logoColor=white" alt="AIOHTTP">
<img src="https://img.shields.io/badge/SciPy-8CAAE6.svg?style=flat&logo=SciPy&logoColor=white" alt="SciPy">
<img src="https://img.shields.io/badge/pandas-150458.svg?style=flat&logo=pandas&logoColor=white" alt="pandas">
<img src="https://img.shields.io/badge/OpenAI-412991.svg?style=flat&logo=OpenAI&logoColor=white" alt="OpenAI">
<img src="https://img.shields.io/badge/Google%20Gemini-8E75B2.svg?style=flat&logo=Google-Gemini&logoColor=white" alt="Google%20Gemini">
<img src="https://img.shields.io/badge/Pydantic-E92063.svg?style=flat&logo=Pydantic&logoColor=white" alt="Pydantic">

</div>
<br>

---

## İçerik

- [Genel Bakış](#genel-bakış)
- [Başlarken](#başlarken)
    - [Ön koşullar](#önkoşullar)
    - [Kurulum](#kurulum)
    - [Çalıştırma](#çalıştırma)
    - [Kullanım](#kullanım)

---

## Genel Bakış

**Tercih Chat**, uygulamalarınızda **ileri seviye doğal dil işleme (NLP)**, **içerik getirme** ve **kullanıcı etkileşimi** süreçlerini kolaylaştırmak için tasarlanmış kapsamlı bir geliştirici araç setidir.  
Birden fazla bileşeni entegre ederek **verimli, doğru ve kullanıcı dostu** dil odaklı işlemler sunar.

---

## 🚀 Servisler ve İş Akışı

Sistem, gelen bir kullanıcı sorgusunu aşağıdaki sıra ile işler:

---

### 1️⃣ Router Servisi
Kullanıcının sorgusunun **amacını (intent)** ve **içerdiği varlıkları (entities)** tespit ederek sonraki servisler için gerekli verileri hazırlar.

- **Intent Classification**  
  - **BERTurk (bert-base-turkish-uncased)** tabanlı, özel olarak eğitilmiş model ile sorgu, önceden tanımlı **niyet listesi** üzerinden analiz edilir.
- **Named Entity Recognition (NER)**  
  - Yine **BERTurk** mimarisi üzerine eğitilmiş NER modeli ile sorgu içerisindeki **yer adları, kurum isimleri, tarih, sayı gibi varlıklar** etiketlenir.
- Çıkan sonuçlar **Retrieve Servisi**ne iletilir.

---

### 2️⃣ Retrieve Servisi (İçerik Getirme)
Kullanıcının sorgusuna uygun bilgileri güvenilir kaynaklardan toplar.

- **Araçlar**: Selenium scraping, Google Custom Search API, Redis caching
- **Kaynaklar**: YÖK Atlas, üniversitelerin resmi siteleri, akademik veri tabanları ve güvenilir web siteleri
- **Cache Mantığı**:  
  - **Cache hit** → Mevcut veri hızlıca getirilir  
  - **Cache miss** → Yeni veriler toplanır, işlenir ve cache’e eklenir
- Toplanan içerikler **Re-ranking Servisi**ne iletilir.

---

### 3️⃣ Re-ranking Servisi
Retrieve Servisi’nden gelen içerikleri iki aşamada yeniden sıralar:

1. **Bi-encoder** ile ön filtreleme  
2. **Cross-encoder** ile alaka puanlaması

Bu işlem sonunda, kullanıcının sorgusuyla **en yüksek alaka düzeyine sahip sonuçlar** belirlenir ve **Gate Servisi**ne gönderilir.

---

### 4️⃣ Gate Servisi
Tüm sürecin **orchestrator** (yöneticisi) olarak çalışır.

- Router, Retrieve ve Re-ranking servislerini **doğru sırayla** çalıştırır
- Re-ranking’den çıkan en alakalı sonuçları, özel eğitilmiş ve **prompt-engineering** ile optimize edilmiş bir **LLM** üzerinden geçirir
- LLM, **rehberlikçi (advisor)** profiline uygun bir üslupla sonuçları sentezler
- Nihai yanıt kullanıcıya iletilir

---

## 🛠️ Teknolojiler
- **Modelleme**: PyTorch, HuggingFace Transformers, BERTurk (bert-base-turkish-uncased)
- **API & Mikroservis**: FastAPI
- **Veri Toplama**: Selenium, Google Custom Search API
- **Cache Yönetimi**: Redis
- **Model Orkestrasyonu**: Python async/await, REST API
- **LLM Çıktı Optimizasyonu**: Prompt Engineering

---

💡 **nlp-deneme**, karmaşık NLP iş akışlarını basitleştirir, yüksek doğrulukta sonuçlar üretir ve kullanıcıya sezgisel, rehberlik odaklı yanıtlar sunar.

---

## Başlarken

### Önkoşullar

Bu proje için aşağıdaki bağımlılıklar gereklidir:

- **Programlama dili:** Python
- **Paket Yönetimi:** Pip

### Kurulum

Bu repoda ki projeyi kullanmak için:

1. **Repoyu cihazına kopyalayın**

    ```sh
    ❯ git clone https://github.com/pulsarTeknoloji/pulsartech_tddi_yarisma.git
    ```

2. **Proje dizinine gidin:**

    ```sh
    ❯ cd "Yarışma Programı"
    ```

3. **Bağımlılıkları yükleyin:**

** Python sanal ortam oluşturun**

```sh
❯ python -m venv venv
```

**Etkinleştirme**
Windows
```sh
❯ venv\Scripts\activate
```

macOS / Linux
```sh
❯ source venv/bin/activate
```

**[pip](https://pypi.org/project/pip/):**

```sh
❯ pip install -r requirements.txt
```

### Çalıştırma

Kullanıcı arayüzünü çalıştırmak için:

```sh
❯ python gui.py
```

Bu program sayesinde ilk başta açılan boot checker gerekli servisleri ve bağımlıkları kontrol edecek eksik varsa sizden izin isteyerek yükleyecektir. Eğer ki servisler çalışmazsa programı durdurun ve sırayla farklı terminallerde tek tek şunları yazın:

**1. terminal**
```sh
❯ python -m uvicorn  retrieve:app --reload --port 8000
```

**2. terminal**
```sh
❯ python -m uvicorn  router:app --reload --port 8001
```

**3. terminal**
```sh
❯ python -m uvicorn  re-rank:app --reload --port 8002
```

**4. terminal**
```sh
❯ python -m uvicorn  gate:app --reload --port 8003
```

Bu sayede servisler tekrar açılacak daha sonrasında ise yine,
Kullanıcı arayüzünü çalıştırmak için:

```sh
❯ python gui.py
```

### Kullanım

Kullancı arayüzü açıldıktan sonra aşağıdaki textbardan model ile konuşabilirsiniz.

---

<div align="left"><a href="#top">⬆ Return</a></div>

---
