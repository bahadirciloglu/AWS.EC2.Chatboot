from langchain_aws import ChatBedrock
from app.llm.config import BEDROCK_MODEL_ID, AWS_REGION

# Model ve bölge ayarları (gerekirse config dosyasından alınabilir)
BEDROCK_MODEL_ID = "anthropic.claude-3-5-sonnet-20241022-v2:0"
AWS_REGION = "us-west-2"

# Bedrock LLM nesnesi
llm = ChatBedrock(
    model_id=BEDROCK_MODEL_ID,
    region_name=AWS_REGION,
    # diğer argümanlar...
    # örn: endpoint_url="https://..."
)
