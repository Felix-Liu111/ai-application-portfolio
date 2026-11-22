import os

from dotenv import load_dotenv
from langchain_ollama import OllamaEmbeddings
from langchain_openai import ChatOpenAI

load_dotenv()

DEEPSEEK_API_KEY_ENV = "DEEPSEEK_API_KEY"
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
DEEPSEEK_CHAT_MODEL = os.getenv("DEEPSEEK_CHAT_MODEL", "deepseek-flash")
DEEPSEEK_PRO_MODEL = os.getenv("DEEPSEEK_PRO_MODEL", "deepseek-v4-pro")

# DeepSeek does not provide an embedding endpoint, so embeddings stay local.
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL", "bge-m3")


def get_chat_model(
    api_key=None,
    base_url=DEEPSEEK_BASE_URL,
    model=DEEPSEEK_CHAT_MODEL,
    temperature=0.7,
    max_tokens=8000,
):
    """Return an OpenAI-compatible DeepSeek chat client."""
    api_key = api_key or os.getenv(DEEPSEEK_API_KEY_ENV)
    if not api_key:
        raise RuntimeError(f"Missing environment variable: {DEEPSEEK_API_KEY_ENV}")
    return ChatOpenAI(
        api_key=api_key,
        base_url=base_url,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )


def get_embeddings():
    """Use local Ollama bge-m3 embeddings."""
    return OllamaEmbeddings(
        base_url=OLLAMA_BASE_URL,
        model=OLLAMA_EMBEDDING_MODEL,
    )
