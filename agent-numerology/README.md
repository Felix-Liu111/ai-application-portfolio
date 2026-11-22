# 命理 Agent

工具调用型对话应用，使用 FastAPI 提供服务，DeepSeek 负责意图判断与回答，Redis 保存多轮会话，Chroma + Ollama `bge-m3` 提供本地知识检索。

## 工具

- 本地风水知识库
- 八字测算
- 每日占卜
- 解梦
- 本地资料不足时明确说明边界

外部搜索工具已移除，不再依赖 SerpAPI。

## 环境要求

- Python 3.11
- Ollama
- Redis
- DeepSeek API Key
- 缘分居 API Key：用于八字、占卜和解梦工具

以下命令以 Windows PowerShell 为例；macOS/Linux 将虚拟环境激活命令替换为 `source .venv/bin/activate`。

## 方式一：本地启动

### 1. 准备 Ollama

```powershell
ollama pull bge-m3
ollama list
```

确认输出包含 `bge-m3`。

### 2. 启动 Redis

已有 Docker Desktop 时，直接使用缓存的 Redis 镜像：

```powershell
docker run -d --name numerology-redis -p 6379:6379 redis:latest
docker exec numerology-redis redis-cli ping
```

预期输出 `PONG`。如果容器名已存在，可改用：

```powershell
docker start numerology-redis
```

### 3. 安装依赖并配置密钥

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
copy .env.example .env
```

编辑 `.env`，填写：

```dotenv
DEEPSEEK_API_KEY=你的DeepSeek密钥
YUANFENJU_API_KEY=你的缘分居密钥
```

仓库不包含真实密钥，`.env` 不要提交到 Git。

### 4. 初始化本地知识库并启动

```powershell
python insert_data_to_chroma.py
python server.py
```

浏览器打开 `http://127.0.0.1:8000`。可以提问“办公室座位正对厕所可以吗？”完成首次验证。

## 方式二：Docker 启动

先复制并填写 `.env`：

```powershell
copy .env.example .env
```

确认 Docker Desktop 正在运行，然后执行：

```powershell
docker compose up --build
```

浏览器打开 `http://127.0.0.1:8001`。停止服务：

```powershell
docker compose down
```

## 常见问题

```powershell
ollama list
docker exec numerology-redis redis-cli ping
```

- 没有 `bge-m3`：执行 `ollama pull bge-m3`
- Redis 校验失败：确认 Docker Desktop 正在运行
- 页面提示缺少密钥：检查 `.env` 中的两个 Key
- 端口被占用：关闭此前启动的同类服务
