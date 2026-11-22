from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from langchain_classic.agents import create_openai_tools_agent, AgentExecutor
from langchain_classic.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from logger import setup_logger
from mytools import *
import os
import traceback
from loguru import logger
from dotenv import load_dotenv
import uuid

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

REDIS_URL = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/')

class Master:
    def __init__(self, chat_message_history=None):
        self.chatmodel = get_chat_model()
        self.MEMORY_KEY = "chat_history"

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """
你是算命大師，說話必用**繁體中文**。
你必須按照「思考→行動→觀察→回答」的步驟來。

規則：
1. 風水 → get_info_from_local_db
2. 八字 → bazi_cesuan
3. 占卜 → yaoyigua
4. 解夢 → jiemeng
5. 其他 → 不要調用工具，明確說明目前資料不足，不要編造。
            """),
            MessagesPlaceholder(variable_name=self.MEMORY_KEY),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        if chat_message_history is not None:
            self.memory = chat_message_history
        else:
            self.memory = RedisChatMessageHistory(url=REDIS_URL, session_id="default_session")

        self.memory_obj = ConversationBufferMemory(
            llm=self.chatmodel,
            human_prefix="用戶",
            ai_prefix="算命大師",
            memory_key=self.MEMORY_KEY,
            output_key="output",
            return_messages=True, #  以消息格式返
            chat_memory=self.memory,# 真正的存储位置（Redis）
        )

        tools = [get_info_from_local_db, bazi_cesuan, yaoyigua, jiemeng]

        agent = create_openai_tools_agent(
            llm=self.chatmodel,
            tools=tools,
            prompt=self.prompt
        )
        # agent = create_react_agent(
        #         llm=self.chatmodel,
        #         tools=tools,
        #         prompt=self.prompt
        #     )
        # 创建执行器，执行并返回结果
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            memory=self.memory_obj,
            verbose=True,
            handle_parsing_errors=True,  # AI 回答格式乱了自动修复,没有他会報错
            return_intermediate_steps=True  # 关键：返回思考过程(Thought（AI 在想什么）Action（AI 决定做什么）Observation（AI 看到了什么结果）)
        )

    def run(self, query):
        logger.info(f"用戶輸入: {query}")
        try:
            result = self.agent_executor.invoke({"input": query})
            logger.info(f"大模型返回: {result}")
            # 组装思考过程 + 最终回答
            thought_log = "認知模式已開啟\n"
            # 把 intermediate_steps 变成思考链展示
            for idx, step in enumerate(result["intermediate_steps"]):
                action = step[0]
                tool_name = action.tool
                tool_input = action.tool_input
                thought_log += f"\n【思考 {idx+1}】：判斷需要使用工具「{tool_name}」"
                thought_log += f"\n【行動】：調用 {tool_name}，參數：{tool_input}"
                thought_log += f"\n【觀察】：取得相關資料\n"

            # 最终回答
            final_answer = result["output"]
            print("思考过程：", thought_log)
            full_response = "\n【算命大師】\n" + final_answer
            return {"output": full_response}

        except Exception as e:
            logger.error(f"異常: {e}")
            return {"output": "天機混亂，請擇日再試。"}

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        query = data.get("query")
        session_id = data.get("session_id", str(uuid.uuid4().hex))
        chat_memory = RedisChatMessageHistory(url=REDIS_URL, session_id=session_id, ttl=600)
        master = Master(chat_memory)
        result = master.run(query)
        return {"session_id": session_id, "output": result["output"]}
    except Exception as e:
        return {"output": "天機不可泄露"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
