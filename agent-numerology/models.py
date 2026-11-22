import os

from dotenv import load_dotenv
from langchain_ollama import OllamaEmbeddings
from langchain_openai import ChatOpenAI

load_dotenv()

DEEPSEEK_API_KEY_ENV = "DEEPSEEK_API_KEY"
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
DEEPSEEK_CHAT_MODEL = os.getenv("DEEPSEEK_CHAT_MODEL", "deepseek-flash")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL", "bge-m3")


def get_chat_model(temperature=0, streaming=True):
    """Return an OpenAI-compatible DeepSeek chat client for tool calling."""
    api_key = os.getenv(DEEPSEEK_API_KEY_ENV)
    if not api_key:
        raise RuntimeError(f"Missing environment variable: {DEEPSEEK_API_KEY_ENV}")
    return ChatOpenAI(
        api_key=api_key,
        base_url=DEEPSEEK_BASE_URL,
        model=DEEPSEEK_CHAT_MODEL,
        temperature=temperature,
        streaming=streaming,
    )


def get_embeddings():
    """Use local Ollama bge-m3 embeddings."""
    return OllamaEmbeddings(
        base_url=OLLAMA_BASE_URL,
        model=OLLAMA_EMBEDDING_MODEL,
    )
