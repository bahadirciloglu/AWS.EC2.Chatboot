import boto3
from langchain.agents import initialize_agent, Tool
from langchain_aws import ChatBedrock
from app.agent.tools import tools  # Tool listesi
from app.llm.config import BEDROCK_MODEL_ID, AWS_REGION
import redis
import os
from ratelimit import limits, sleep_and_retry
from tenacity import retry, wait_exponential, stop_after_attempt
import queue
import threading
import json

# Redis bağlantısı
r = redis.Redis(host='localhost', port=6379, db=0)

def add_user_message(user_id, message):
    """Kullanıcıya ait mesajı geçmişe ekle."""
    r.rpush(f"user:{user_id}:history", message)

def get_user_history(user_id):
    """Kullanıcıya ait mesaj geçmişini getir."""
    history = r.lrange(f"user:{user_id}:history", 0, -1)
    return [msg.decode() for msg in history]

def clear_user_history(user_id):
    """Kullanıcıya ait mesaj geçmişini sil."""
    r.delete(f"user:{user_id}:history")

# Agent başlatma
llm = ChatBedrock(model_id=BEDROCK_MODEL_ID, region_name=AWS_REGION)

tool_objs = [Tool(name=t["name"], func=t["func"], description=t["description"]) for t in tools]

agent = initialize_agent(
    tools=tool_objs,
    llm=llm,
    agent_type="openai-functions",
    verbose=True
)

SYSTEM_PROMPT = (
    "Sen güvenilir ve uzman bir Türkçe Soru-Cevap asistanısın.\n"
    "Her zaman sadece Türkçe dilinde cevap ver.\n"
    "Eğer kullanıcıdan gelen soru Türkçe değilse, cevap olarak sadece şunu ver:\n"
    "Merhaba, sadece Türkçe dilinde hizmet vermekteyim.\n"
    "Aşağıdaki konular hakkında size yardımcı olabilirim:\n"
    "1. Chatbot\n"
    "2. Sesli asistan\n"
    "3. Servis robot entegrasyonu\n"
    "4. Temizlik robot entegrasyonu\n"
    "Ya da bize ulaşabilirsiniz, Tel: 05075135234 Email: bahadir@kartal.ai\n"
    "Ek kurallar:\n"
    "- Sadece bilgi tabanındaki içeriklere göre cevap ver.\n"
    "- Bilgi tabanında içerik yoksa, 'Üzgünüm, bu konuda bilgi tabanımda bir içerik bulamadım. Lütfen daha farklı veya detaylı bir soru sorabilirsiniz.' de.\n"
    "- Asla contexti doğrudan referans gösterme.\n"
    "- Yanıtlarının doğruluğunu garanti edemezsin, öneri niteliğindedir.\n"
    "- Emin olmadığın veya bilmediğin konularda 'Bu konuda kesin bir bilgim yok.' de, tahmin yürütme, yanlış bilgi verme.\n"
    "- Küfür, hakaret, ayrımcılık, cinsellik, şiddet gibi uygunsuz içerik üretme. Kullanıcıya karşı her zaman saygılı ve nazik ol.\n"
    "- Tıbbi, hukuki, finansal veya kritik kararlar için yanıt verme. Kişisel veri, şifre, kredi kartı gibi hassas bilgi isteme veya kaydetme.\n"
    "- Tarafsız ve önyargısız yanıtlar ver. Hiçbir kişi, kurum, topluluk veya ülke hakkında ayrımcı, önyargılı veya taraflı ifadeler kullanma.\n"
    "- Yanıtlarını kısa, öz ve anlaşılır tut. Gereksiz detaylardan kaçın.\n"
    "- Mümkünse, verdiğin bilgilerin kaynağını belirt. Kaynağı olmayan bilgileri açıkça belirt."
)

def run_agent(user_input):
    prompt = f"{SYSTEM_PROMPT}\n\nKullanıcı sorusu: {user_input}"
    response = agent.run(prompt)
    # Sistem mesajı, karşılama veya bilgi yoksa özel mesajı döndür
    if (
        response.strip().startswith("Merhaba!") or
        "talimat" in response or
        "sadece Türkçe" in response or
        "bilgi tabanındaki içeriklere göre" in response or
        response.strip().startswith("Üzgünüm")
    ):
        return (
            "Merhaba, sorunuzu anlayamadım. Size aşağıdaki konularda yardımcı olabilirim:\n\n"
            "1. Chatbot\n"
            "2. Sesli asistan\n"
            "3. Servis robot entegrasyonu\n"
            "4. Temizlik robot entegrasyonu\n\n"
            "İletişim için:\n"
            "Tel: 05075135234\n"
            "Email: bahadir@kartal.ai"
        )
    return response

# Yeni mesaj geldiğinde:
user_id = "user123"
user_message = "Merhaba!"
add_user_message(user_id, user_message)

# Geçmişi okuma:
history = get_user_history(user_id)
print(history)

# Geçmişi silme:
clear_user_history(user_id)

# Örnek: context_list, arama sonucu dönen context'ler
# max_score, dönen context'lerin en yüksek benzerlik skoru

def handle_no_context(request, context_list, max_score, threshold):
    logger.info(f"Context bulunamadı. Soru: {request.message}") # type: ignore
    return {"response": (
        "Üzgünüz, bu konuda detaylı bilgi sağlayamıyoruz.\n"
        "Size aşağıdaki konularda yardımcı olabilirim:\n"
        "1. Chatbot\n"
        "2. Sesli asistan\n"
        "3. Servis robot entegrasyonu\n"
        "4. Temizlik robot entegrasyonu\n"
        "Lütfen bu konulardan birini seçerek tekrar sorabilirsiniz.\n"
        "Ya da bize ulaşabilirsiniz:\n"
        "Tel: 05075135234\n"
        "Email: bahadir@kartal.ai"
    )}

@sleep_and_retry
@limits(calls=10, period=1)  # 1 saniyede en fazla 10 çağrı
@retry(wait=wait_exponential(multiplier=1, min=1, max=10), stop=stop_after_attempt(5))
def call_bedrock_api(prompt, model_id, region_name):
    # Bedrock API çağrısı
    bedrock_client = boto3.client('bedrock-runtime', region_name=region_name)
    response = bedrock_client.invoke_model(
        modelId=model_id,
        body=json.dumps({
            "prompt": prompt,
            "maxTokens": 512,
            "temperature": 0.7,
            "topP": 0.9,
        })
    )
    return json.loads(response['body'].read())

bedrock_queue = queue.Queue()

def bedrock_worker():
    while True:
        args = bedrock_queue.get()
        call_bedrock_api(*args)
        bedrock_queue.task_done()

threading.Thread(target=bedrock_worker, daemon=True).start()
# API endpoint'inde:
def api_endpoint(prompt: str, model_id: str, region_name: str):
    bedrock_queue.put((prompt, model_id, region_name))  # Bedrock'a gidecek istekler kuyruğa eklenir
