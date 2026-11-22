# RAG 文档问答

支持 `docx`、`pdf`、`txt`、`csv` 和 `md` 文档上传，使用 Chroma 与 BM25 混合检索，由 DeepSeek 生成回答。

## 功能

- 文档加载、递归切分与索引
- Ollama `bge-m3` 本地向量化
- 向量检索与 BM25 关键词检索
- 查询改写与相关性过滤
- DeepSeek `deepseek-flash` / `deepseek-v4-pro`
- RAGAS 指标评估示例

当前演示版本没有接入独立重排模型，暂由查询改写与相关性过滤完成上下文整理。

## 环境要求

- Python 3.11
- Ollama
- DeepSeek API Key

以下命令以 Windows PowerShell 为例；macOS/Linux 将虚拟环境激活命令替换为 `source .venv/bin/activate`。

## 1. 准备 Ollama

```powershell
ollama pull bge-m3
ollama list
```

确认输出包含 `bge-m3`。如果 Ollama 没有运行，先执行：

```powershell
ollama serve
```

## 2. 安装依赖与配置密钥

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
copy .env.example .env
```

编辑 `.env`，填写自己的 DeepSeek Key：

```dotenv
DEEPSEEK_API_KEY=你的密钥
```

仓库不包含真实密钥，`.env` 不要提交到 Git。

## 3. 启动

```powershell
python main.py
```

浏览器打开 `http://127.0.0.1:7860`。

上传 [`sample-data/demo.md`](sample-data/demo.md)，选择对应知识库，然后提问“出差住宿标准是多少？”即可完成首次验证。

## RAGAS 示例

先把待评估文档放入 `chroma/knowledge/`，然后执行：

```powershell
python rags_eval.py
```

当前脚本使用一条示例问题和参考答案，只用于验证评估链路，不代表正式测试集结果。
