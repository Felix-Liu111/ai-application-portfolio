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

## 启动

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
copy .env.example .env
ollama pull bge-m3
python main.py
```

启动前在 `.env` 中填写 `DEEPSEEK_API_KEY`。

## RAGAS 示例

先把待评估文档放入 `chroma/knowledge/`，然后执行：

```powershell
python rags_eval.py
```

当前脚本使用一条示例问题和参考答案，只用于验证评估链路，不代表正式测试集结果。
