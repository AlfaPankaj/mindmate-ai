from langchain_nvidia_ai_endpoints import ChatNVIDIA
from core.config import get_settings

settings = get_settings()

def get_llm():
    settings = get_settings()
    model = getattr(settings, "MODEL_NAME", "meta/llama-3.3-70b-instruct")
    
    if not settings.NVIDIA_API_KEY or "your-key-here" in settings.NVIDIA_API_KEY:
        raise ValueError("❌ NVIDIA_API_KEY is missing or invalid in your .env file. Please add your key from build.nvidia.com.")
        
    return ChatNVIDIA(
        model=model,
        nvidia_api_key=settings.NVIDIA_API_KEY,
        temperature=0.2,
        max_tokens=1024
    )
