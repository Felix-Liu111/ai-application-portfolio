
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.tools import tool
from langchain_chroma import Chroma
from langchain_core.output_parsers import JsonOutputParser
import requests
from models import get_chat_model, get_embeddings
import os

YUANFENJU_API_KEY = os.getenv("YUANFENJU_API_KEY")

@tool
def get_info_from_local_db(query: str):
    """專門查「辦公室風水」「風水常識」相關內容。"""
    vector_store = Chroma(
        persist_directory="./chroma_db",
        embedding_function=get_embeddings(),
        collection_name="local_documents"
    )
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})
    docs = retriever.invoke(query)
    return [d.page_content for d in docs]

@tool
def bazi_cesuan(query: str):
    """用戶要算八字、排八字、論命、看命盤時使用。需要姓名 + 出生年月日時。"""
    if not YUANFENJU_API_KEY:
        return "今日天門已閉，改日再來。"
    url = "https://api.yuanfenju.com/index.php/v1/Bazi/cesuan"
    prompt = ChatPromptTemplate.from_template("""
提取參數：姓名、性別、公曆/農曆、出生年月日時。
JSON格式：
{{
  "api_key": "{api_key}",
  "name": "姓名",
  "sex": "0男1女",
  "type": "1",
  "year": "年",
  "month": "月",
  "day": "日",
  "hours": "時",
  "minute": "0"
}}
用戶輸入：{query}
""")
    parser = JsonOutputParser()
    chain = prompt | get_chat_model(streaming=False) | parser
    data = chain.invoke({"query": query, "api_key": YUANFENJU_API_KEY})
    res = requests.post(url, data=data)
    if res.status_code == 200:
        j = res.json()
        return "八字為：" + j["data"]["bazi_info"]["bazi"]
    return "八字查詢失敗，請提供姓名與出生年月日時。"

@tool
def yaoyigua():
    """用戶想要占卜、求籤、搖卦、問運勢時使用。"""
    url = "https://api.yuanfenju.com/index.php/v1/Zhanbu/meiri"
    res = requests.post(url, data={"api_key": YUANFENJU_API_KEY})
    if res.status_code == 200:
        return res.json()["data"]["description"]
    return "占卜暫不可用。"

@tool
def jiemeng(query: str):
    """用戶做夢、想解夢、詢問夢境含義時使用。"""
    url = "https://api.yuanfenju.com/index.php/v1/Gongju/zhougong"
    llm = get_chat_model(streaming=False)
    kw = llm.invoke(f"提取夢境關鍵詞：{query}")
    res = requests.post(url, data={"api_key": YUANFENJU_API_KEY, "title_zhougong": kw})
    if res.status_code == 200:
        return res.json()
    return "解夢服務暫不可用。"
