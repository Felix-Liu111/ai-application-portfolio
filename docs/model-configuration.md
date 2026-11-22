# 模型分工

## 当前配置

| 能力 | 运行位置 | 默认模型 | 原因 |
| --- | --- | --- | --- |
| 对话与任务理解 | DeepSeek API | `deepseek-flash` | 响应速度快，支持工具调用 |
| 质量优先的对话模型 | DeepSeek API | `deepseek-v4-pro` | RAG 中可按需切换 |
| 文档嵌入 | 本机 Ollama | `bge-m3` | 中文与多语言检索，不消耗 DashScope 额度 |
| 向量数据库 | 本机 | Chroma | 保存文档向量与索引 |

## 为什么这样拆分

DeepSeek 负责文本理解、查询改写、工具选择与回答生成，但不负责向量嵌入。RAG 仍需要把文档转换为向量，因此使用本机 Ollama 的 `bge-m3`。这种拆分让云端模型与本地检索各自完成擅长的任务。

## 启动前提

```text
ollama serve
ollama pull bge-m3
```

外网模型调用只读取环境变量中的 DeepSeek Key。密钥不写入代码、文档或仓库。

## 已验证

- `bge-m3` 在本机返回 1024 维嵌入。
- `deepseek-flash` 和 `deepseek-v4-pro` 均可通过当前 DeepSeek 接口完成工具调用。
- 默认对话模型使用 `deepseek-flash`，避免命理 Agent 在每次工具调用时使用更重的模型。
