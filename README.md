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
- [Başlarken](#baslarken)
    - [Önkoşullar](#onkosullar)
    - [Kurulum](#kurulum)
    - [Çalıştırma](#calistirma)
    - [Kullanım](#kullanim)

---

## Genel Bakış

Bu repo, uygulamalarınızda gelişmiş türkçe doğal dil işleme, içerik getirme ve kullanıcı etkileşimini kolaylaştırmak için tasarlanmış kapsamlı bir geliştirici araç setidir.
Birden fazla bileşeni entegre ederek verimli, doğru ve kullanıcı dostu dil odaklı işlemler sunar.

**Neden Tercih Chat**

Bu proje, karmaşık NLP iş akışlarını basitleştirmeyi ve arama ile içerik anlama yeteneklerini geliştirmeyi amaçlamaktadır.
Temel özellikleri şunlardır:

- 🧩 **🔍 Re-ranking Servisi:** Implements a two-stage process with bi-encoder filtering and cross-encoder scoring to refine search results for higher relevance.
- 🌐 **🕸️ Content Retrieval:** Combines Selenium scraping, Google Custom Search, and Redis caching for scalable, targeted web content extraction.
- 🎨 **🖥️ User Interface:** Provides an intuitive GUI for seamless data input, processing, and output visualization.
- ⚙️ **🤖 Microservice Orchestration:** Manages interactions between NLP models, retrieval systems, and response generation within a modular architecture.
- 🚀 **🚦 FastAPI Routing:** Handles dynamic query classification, intent detection, and context-aware response generation efficiently.

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
