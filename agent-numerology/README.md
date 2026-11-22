# 命理 Agent

工具调用型对话应用，使用 FastAPI 提供服务，DeepSeek 负责意图判断与回答，Redis 保存多轮会话，Chroma + Ollama `bge-m3` 提供本地知识检索。

## 工具

- 本地风水知识库
- 八字测算
- 每日占卜
- 解梦
- 本地资料不足时明确说明边界

外部搜索工具已移除，不再依赖 SerpAPI。

## 本地启动

仓库不包含真实密钥。启动前复制 `.env.example` 为 `.env`，由运行者自行填写：

- `DEEPSEEK_API_KEY`：用于对话和工具选择
- `YUANFENJU_API_KEY`：用于八字、占卜和解梦工具

Ollama 和 Redis 在本地运行，不需要 API Key。

先在 Ollama 中准备嵌入模型：

```powershell
ollama pull bge-m3
```

启动 Redis：

```powershell
docker run -d --name numerology-redis -p 6379:6379 redis:latest
```

启动应用：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
copy .env.example .env
python insert_data_to_chroma.py
python server.py
```

访问 `http://127.0.0.1:8000`。

## Docker

```powershell
copy .env.example .env
docker compose up --build
```

访问 `http://127.0.0.1:8001`。
