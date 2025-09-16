ssh -i new.pem ec2-user@34.222.232.114
cd ~/ec2-c
source venv/bin/activate
python tests/test_chat.py
 uvicorn app.main:app --host 0.0.0.0 --port 8000  --reload --log-level debug
PYTHONPATH=$(pwd) pytest tests/test_chat_api.py
PYTHONPATH=$(pwd) pytest tests/test_api.py
PYTHONPATH=$(pwd) pytest tests/test_api_call.py

PYTHONPATH=$(pwd) pytest tests/test_prompt_context.py
PYTHONPATH=$(pwd) pytest tests/test_rag_corpus.py
PYTHONPATH=$(pwd) pytest tests/test_redis_connection.py
PYTHONPATH=$(pwd) pytest tests/test_redis_integration.py
PYTHONPATH=$(pwd) pytest tests/test_redis_utils.py
PYTHONPATH=$(pwd) pytest tests/test_user_state.py
PYTHONPATH=$(pwd) pytest tests/test_utils.py
uvicorn app.main:app --host 0.0.0.0 --port 8000


http://localhost:8000/health → Backend ayakta mı?
http://localhost:8000/test-redis → Redis bağlantısı çalışıyor mu?
http://localhost:8000/test-bedrock → Bedrock bağlantısı çalışıyor mu?
http://localhost:8000/docs
API endpoint'lerini elle ve otomatik test et.
ssh -i new.pem ec2-user@34.222.232.114
cd ~/ec2-c
source venv/bin/activate
PYTHONPATH=$(pwd) pytest tests/test_api.py
pip install -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html
python setup_index.py - bir kereye mahsus rag verilerini embeed edip indekledik.
uvicorn app.main:app --host 0.0.0.0 --port 8000
Kontrol Komutları
Disk alanı:  df -h = 25/ 2 G/11 G/
Bellek:  free -h = 1.9/1.5 GB/
CPU:  lscpu = 1 - Intel Xeon E5-2686 v4
uygulamanın toplam disk boyutu : 1.4 G


FastAPI/Pydantic ERROR 
- [x]Tüm FastAPI endpoint fonksiyonlarını (@app.post, @app.get, vs.) bul.
POST Endpointleri
@app.post("/rag-query") - Pydantic model (SoruModel) alıyor, framework objesi yok.
@app.post("/chat", response_model=ChatResponse) - Pydantic model (ChatRequest) alıyor,framework objesi yok.
@app.post("/endpoint") - Pydantic model (MyInput) alıyor,framework objesi yok.
@app.post("/ornek") - Parametre yok.
GET Endpointleri
@app.get("/welcome") - Parametre yok.Sadace fonksiyon amaçlı.
@app.get("/health") - Parametre yok.Sadace fonksiyon amaçlı.
@app.get("/test-redis")- Parametre yok.Sadace fonksiyon amaçlı.
@app.get("/test-bedrock")- Parametre yok.Sadace fonksiyon amaçlı.


- [x]Tüm Pydantic modellerini (BaseModel türevleri) bul. c/app/api/routes.py , c/app/schemas/chat.py ve c/app/main.py de Pydantic model ve endpoint parametre kullanımları tamamen doğru, ramework objesi içeren model veya yanlış parametre sıralaması yok.

- [x]Model içinde framework objesi (Request, Response, vs.) olup olmadığını kontrol et.
        app/schemas/chat.py : Bu dosyada Pydantic modelleri (ChatRequest, ChatResponse) tanımlı.Kontrol:Her iki modelin alanları sadece temel veri tipleri (str).Framework objesi yok, kullanım doğru

        app/main.py : Pydantic modelleri (SoruModel, ChatRequest, ChatResponse, MyInput) tanımlı.üm modellerin alanları sadece temel veri tipleri (str).Kullanım doğru.

        app/agent/, app/llm/, app/services/, app/rag/, app/api/ Bu dizinlerde de model (BaseModel türevi) tanımı içeren bir dosya yok.

- [x]Gereksiz Parametreleri Kaldır
Eğer endpointte request: Request kullanılmıyorsa, parametre listesinden çıkar.
app/main.py-Gereksiz request: Request parametresi yok, kaldırılacak bir şey yok., app/api/routes-py-Burada da gereksiz framework objesi parametresi yok. , app/agent/agent.py, app/agent/tools.py, app/services/session.py - Kontrol gerektiren bir durum yok.



## A. Yerel Geliştirme ve Test

### 1. Mimari ve Altyapı (Yerel)
- [x] Geliştirme ortamının hazırlanması (Python, pip, virtualenv)
- [x] .env ve gizli anahtarların yerel olarak yapılandırılması
- [x] Vektör veritabanı (Chromadb) yerel kurulumu
- [x] AWS Bedrock erişimi için yerel kimlik bilgisi ayarları

### 2. API ve Backend (Yerel)
- [x] FastAPI endpointlerinin (özellikle /chat) yerelde çalışır hale getirilmesi
- [x] Swagger/OpenAPI dokümantasyonunun yerelde test edilmesi
- [x] Yerel loglama ve hata yönetimi

### 3. Agentic LLM ve Akış Yönetimi (Yerel)
- [x] LangChain ile agent, tool ve function tanımlarının yerelde test edilmesi
- [x] LlamaIndex ile bilgi tabanı (RAG corpus) entegrasyonu ve yerel testleri
- [x] Prompt ve context yönetiminin yerelde doğrulanması
        Prompt ve context dosyalarını oku.
        Kullanıcı girdisiyle birleştir.
        Son promptu ekrana/loga yaz.
        Gözle veya otomatik testle kontrol et.
        Model çağrısı yapmadan önce hatalı birleştirme varsa düzelt.
- [x] Kullanıcı geçmişi ve state yönetimi (opsiyonel: Redis ile) yerelde test edilmesi
        Python'da Redis bağlantısı (ör. redis-py ile)
        Kullanıcı geçmişi/state okuma-yazma
        Test kodu veya entegrasyon 
- [x] Q&A verisinin rag_corpus ile bütünleştirilmesi ve yerel testleri

4. Test ve Doğrulama (Yerel)
- [x] Birim ve entegrasyon testlerinin yazılması (pytest, httpx)


5.Fonksiyonel (Kullanıcı) Testleri
- [x] Temel Soru-Cevap Testi:Farklı, basit ve karmaşık sorular sorarak yanıtların mantıklı ve beklenen şekilde olup olmadığını kontrol et.
        Test Senaryoları Hazırla
        Basit sorular:
        "Merhaba", "Nasılsın?", "Bugün hava nasıl?"
        Karmaşık sorular:
        "Otel robotlarının avantajları nelerdir?",
        "Bir otelde robotik oda servisi nasıl çalışır?",
        "RAG tabanlı sistemlerde embedding modeli neden önemlidir?"
        Alakasız/absürt sorular:
        "Ayakkabım kaç numara?",
        "Uzayda pizza yenir mi?"


- [x] RAG (Belge Arama) Testi:Bilgi tabanında kesinlikle olan bir soruyu sor ve doğru cevabın döndüğünden emin ol.
Bilgi tabanında olmayan, alakasız bir soru sor ve modelin uygun şekilde "bilmiyorum" veya "bilgi yok" yanıtı verip vermediğini kontrol et.
        Ajansınız ne iş yapıyor?
        Hangi hizmetleri sunuyorsunuz?
        AI ve robotik alanında hangi teknolojileri kullanıyorsunuz?
        Ajansınız nerede bulunuyor?
        Çalışma saatleriniz nedir?

Kullanıcı Soru Soruyor
        ↓
Backend (API/Gradio)
        ↓
Soru → Embedding Modeli → Vektör Arama (RAG) → En Yakın Context(ler)
        ↓
Context + Soru → LLM (Claude, GPT, vs.)
        ↓
    LLM Yanıtı
        ↓
     Backend
        ↓
Kullanıcıya Yanıt

- [x] Kullanıcıdan gelen her soruda, seçilen context'leri ve similarity skorlarını logla.
- [x] "Ajansınız ne iş yapıyor?" sorusunda, context'te gerçekten q&a.json'daki doğru cevabın olup olmadığını kontrol et.
- [x] LLM'e gönderilen prompt'un içinde context'in olup olmadığını logla.
- [x] Vektör arama eşik değerini düşürüp, daha fazla context iletmeyi dene.
- [x] Türkçe sorularda doğru çalışıp çalışmadığını basit örneklerle test et.
- [x] Çoklu Dil Testi (varsa):Uygulaman çoklu dil destekliyorsa, farklı dillerde sorular sor.
        İngilizce: "What is an pencil?"
        Almanca: "Was ist ein pencil?"
        Fransızca: "Qu'est-ce qu'un pencil?"
- [x] Uzun Soru/Metin Testi: Çok uzun veya çok kısa sorularla sistemi test et.
{
  "user_id": "test_user_long",
  "message": "Yapay zeka ve makine öğrenimi teknolojilerinin tarihsel gelişimi, günümüzdeki uygulama alanları, avantajları ve dezavantajları hakkında detaylı bilgi verebilir misiniz? Özellikle yazılım ajanlarının evrimi, kullanım örnekleri, karşılaşılan zorluklar ve bu teknolojilerin sağlık, finans, eğitim, üretim, ulaşım gibi sektörlerdeki etkileriyle birlikte, etik ve yasal boyutları da dahil olmak üzere kapsamlı bir açıklama yapar mısınız? Ayrıca, gelecekte yapay zeka teknolojilerinin hangi alanlarda daha fazla gelişme göstereceği ve bu gelişmelerin toplumsal, ekonomik ve kültürel etkileri hakkında öngörüleriniz nelerdir? Lütfen mümkünse güncel uygulama örnekleri ve karşılaşılan pratik sorunlara da değinin."
}
        Sonuçları Değerlendir
                Uzun ve kısa girdilerde sistemin:
                Hata yönetimi
                Yanıt kalitesi
                Performansı
                Kullanıcı deneyimi

- [x] Boş Soru Testi:Hiçbir şey yazmadan veya sadece boşluk karakterleriyle istek gönder.
        {
        "user_id": "test",
        "message": ""
        }

        {
        "user_id": "test",
        "message": "     "
        }

- [x] Özel Karakter/Emoji Testi: Soruya özel karakterler, emojiler veya unicode karakterler ekle.
        Artificial Intelligence nedir? 🤖
        Artificial Intelligence hakkında bilgi verir misin? 🚀✨

8.Kullanıcı Deneyimi (UX) Testleri
- [x] Yanıt Süresi:
Yanıtların hızlı ve tutarlı gelip gelmediğini gözlemle
- [x] Hata Mesajları:
Hatalı inputlarda kullanıcıya gösterilen hata mesajlarının açıklayıcı ve kullanıcı dostu olup olmadığını kontrol et.
- [x] Arayüz Akışı:
Soru sorma, yanıt alma, flagleme (işaretleme) gibi akışların sorunsuz çalıştığından emin ol.
- [x]Flag Butonu:
Yanlış veya uygunsuz bir yanıtı flagleyip, flagged klasörüne kaydedildiğinden emin ol.
- [x]
Flaglenen Yanıtların İncelenmesi:
flagged/ klasöründeki dosyaları açıp, flaglenen örneklerin doğru kaydedildiğini kontrol et.
- [x]Çoklu Kullanıcı:
Farklı tarayıcılardan veya cihazlardan aynı anda soru sorarak uygulamanın çoklu kullanıcıya yanıt verip veremediğini test et.
- [x]Yük Testi:
Otomasyon araçlarıyla (ör. Selenium, Locust, k6) çok sayıda istek göndererek sistemin yanıt süresini ve stabilitesini ölç.
- [x]XSS/Injection Testi:
Input alanına <script>, SQL injection gibi zararlı kodlar girerek sistemin bunları filtreleyip filtrelemediğini test et.
- [x]Rate Limiting:
Çok hızlı ve çok sayıda istek göndererek sistemin rate limit veya throttling uygulayıp uygulamadığını gözlemle.
- [x]Mobil Uyumluluk:
Gradio arayüzünü mobil cihazda açıp, arayüzün düzgün görünüp görünmediğini test et.
- [x]Farklı Tarayıcılar:
Chrome, Firefox, Safari gibi farklı tarayıcılarda arayüzün ve fonksiyonların sorunsuz çalıştığından emin ol.
- [x]Logları İncele:
app.log ve terminal çıktısında beklenmeyen hata veya uyarı olup olmadığını kontrol et.
- [x]Hata Durumunda Log Kaydı:
Bilinçli olarak hata oluşturup, logda düzgün kaydedildiğinden emin ol.
- [x]Kullanıcı Geçmişi/State Testi (Varsa)
Kullanıcıya özel geçmiş veya state tutuluyorsa, farklı kullanıcılarla giriş yapıp, geçmişin doğru tutulup tutulmadığını test et.


## B. AWS EC2'ya Yayın ve Canlıya Alma

### 1. Altyapı ve Ortam Kurulumu (EC2)
- [x] AWS EC2 instance oluşturulması ve gerekli portların açılması
- [x] Proje dosyalarının EC2'ya aktarılması
- [x] Sanal ortam kurulumu ve bağımlılıkların yüklenmesi (requirements.txt)
- [x] Testlerin yapılması.
### 2. API ve Backend (EC2)
- [x] FastAPI uygulamasının EC2 üzerinde başlatılması
### 3. Test ve Doğrulama (EC2)
- [x] API endpointlerinin EC2 ortamında test edilmesi
- [x] LLM ve bilgi tabanı entegrasyonunun EC2'da doğrulanması



**Canlıya alırken backend’i HTTPS ile sunmak için Nginx + SSL (Let’s Encrypt) yapılandır.**

- [x] İş Paketi: api.conf’u Sadece HTTP (80) için Yapılandır , /etc/nginx/conf.d/api.conf dosyasını aşağıdaki gibi düzenleyin:    
server {
        listen 80;
        server_name api.aws.chatbot;

        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
    Nginx konfigürasyonunu test edin ve yeniden başlatın:    sudo nginx -t
    sudo systemctl restart nginx
    curl -i -X POST http://api.aws.chatbot/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user", "message": "Merhaba"}'

- [x] Alan Adı için SSL Sertifikası Al ve HTTPS (443) ile Yapılandır  ,Let’s Encrypt ile SSL sertifikası alın:
    sudo certbot --nginx -d api.aws.chatbot
Bu komut, Nginx konfigürasyonunu otomatik olarak günceller ve 443 portunu aktif eder.
Test:
curl -i -X POST https://api.aws.chatbot/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user", "message": "Merhaba"}'



- [x] 80 ve 443 Portlarından Uygulamaya Erişim Testi ve Son Konfigürasyon Kontrolü
Hem HTTP (80) hem HTTPS (443) portlarından erişimi test edin:    curl -I http://api.aws.chatbot
    curl -I https://api.aws.chatbot
80 portundan gelen isteklerin otomatik olarak 443’e yönlendiğinden (redirect) ve HTTPS ile API yanıtı döndüğünden emin olun.
Nginx konfigürasyonunu tekrar kontrol edin, gerekirse 80’den 443’e yönlendirme ekleyin:    server {
        listen 80;
        server_name api.aws.chatbot;
        return 301 https://$host$request_uri;
    }


- [x] Canlıda (https://www.aws.chatbot) Tarayıcıdan API’ye İstek At ve Son Kontrol
Frontend (ör. Vercel’deki) uygulamanızdan, canlıda https://api.aws.chatbot/chat adresine istek atın.
Tarayıcıda CORS, SSL ve API yanıtı ile ilgili bir hata olup olmadığını kontrol edin.
Gerekirse CORS ayarlarını FastAPI’de güncelleyin:
    from fastapi.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://www.aws.chatbot"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    Z RAPORU
API endpoint’leriniz (ör. /chat, /health, vs.) hem doğrudan hem de reverse proxy (https://api.aws.chatbot) üzerinden erişilebilir durumda.
CORS ve preflight (OPTIONS) istekleri doğru şekilde yanıtlanıyor.
Nginx ve FastAPI loglarında istekler ve yanıtlar beklenen şekilde görünüyor.
WS Bedrock gibi harici servislerden gelen throttling hataları dışında altyapı tarafında bir sorun yok.

- [x] Kullanıcı kimliği (user_id/session_id) yönetimi ve iletimi
        Frontendde : . user_id ve session_id Üretimi ve Saklanması
        user_id:
        İlk ziyaret/ilk yüklemede rastgele bir UUID üret.
        localStorage’da sakla (tarayıcı kapansa da kalıcı olur).
        session_id:
        Her yeni oturumda (veya sayfa yenilendiğinde) rastgele bir UUID üret.
        sessionStorage’da sakla (sekme/oturum kapandığında silinir).
        Örnek Kod:function getOrCreateUserId() {
  let userId = localStorage.getItem("user_id");
  if (!userId) {
    userId = crypto.randomUUID();
    localStorage.setItem("user_id", userId);
  }
  return userId;
}

function getOrCreateSessionId() {
  let sessionId = sessionStorage.getItem("session_id");
  if (!sessionId) {
    sessionId = crypto.randomUUID();
    sessionStorage.setItem("session_id", sessionId);
  }
  return sessionId;
}
er API Çağrısında Bu Kimlikleri Gönder
API’ye yapılan her istekte (ör. /chat), body içinde user_id ve session_id’yi gönder.
Örnek Kod:fetch("https://api.aws.chatbot/chat", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    user_id: getOrCreateUserId(),
    session_id: getOrCreateSessionId(),
    message: "Merhaba"
  })
});

- [x] Backend’de Yapılacaklar
1. Kimlikleri Endpoint’te Almak
FastAPI endpoint’inde, gelen request’te user_id ve session_id’yi al.
Örnek Kod:from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    # Kimlikleri kullan
    ...
    2. Kimlikleri Loglamak ve Analiz İçin Kullanmak
Her istekte user_id ve session_id’yi logla.
Kişiselleştirme, rate limit, abuse detection gibi işlemler için bu kimlikleri kullan.
Örnek Kod:import logging

@app.post("/chat")
async def chat(request: ChatRequest):
    logging.info(f"User: {request.user_id}, Session: {request.session_id}, Message: {request.message}")
    # ... iş mantığı ...
    return {"response": "Cevabınız burada", "session_id": request.session_id}


        Backend’de: 3. Kimliklerin Alınması, Loglanması ve Kullanılması Backend’de yapılmalı. FastAPI endpoint’inde gelen request’te user_id ve session_id alınır. Loglama, kişiselleştirme, rate limit, analiz gibi işlemler backend’de yapılır.



- [x] Farklı tarayıcı ve cihazlarda entegrasyonun doğrulanması

- [x] Hatalı/güvensiz isteklerin doğru şekilde reddedildiğinin test edilmesi

- [x] Widget'ta ve backend'de hata mesajlarının kullanıcı dostu şekilde gösterilmesi

- [x] Bağlantı kopması, rate limit, backend hatası gibi durumlarda uygun uyarıların verilmesi

- [x] AWS CloudWatch ile EC2 kaynak kullanımı ve log takibi




- [x]Dokümantasyon ve Yayın Öncesi Hazırlık readme.md ve teknik dökümantasyonun güncellenmesi

- [x] Kullanıcı ve geliştirici kılavuzlarının hazırlanması


- [ ] Security konularına hakim olduk sıra chatbot sohbet akışı değişecek ve gelişecek.


- [ ] Sheet ID = 140rnsQd4rZrK2YMPW_XUT2TAq0tWso2her-xqfpjLiI
- [ ] script ne durumda , scriptte hangi sabit değerler yer değiştirmeli
- [ ] service_account.json dosyası script ile aynı dizinde
- [ ] Gerekli Python paketleri (gspread, google-auth) kurulu.