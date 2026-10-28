# RagProjectPractice

基于 LangChain + 通义千问（DashScope）+ Chroma 的 RAG 知识库问答练习项目，使用 Streamlit 提供交互界面。

## 功能

- 上传 txt 文件，自动切块并存入 Chroma 向量库，通过 MD5 去重避免重复入库
- 基于向量检索的问答，回答以流式方式输出
- 支持多轮对话，聊天历史持久化到本地文件
- 两个独立页面：知识库上传、聊天问答

## 项目结构

```
.
├── app_file_upload.py                     # 知识库上传页面（Streamlit）
├── app_mian.py                            # 聊天问答页面（Streamlit）
├── knowledge_base.py                      # 文本切块、向量入库、MD5 去重
├── rag.py                                 # RAG 链：检索 + 提示词 + 通义千问
├── vector_govern_and_discover_service.py  # 向量库检索器封装
├── file_history_storage.py                # 基于文件的聊天历史存储
├── chroma_db/                             # Chroma 本地持久化数据
├── history_storage/                       # 聊天历史数据
└── md5.txt                                # 已上传内容的 MD5 记录
```

## 技术栈

- [LangChain](https://python.langchain.com/) — RAG 链编排、文本切分、对话历史管理
- [通义千问 DashScope](https://dashscope.aliyun.com/) — 对话模型 `qwen3.7-max`、嵌入模型 `text-embedding-v1`
- [Chroma](https://www.trychroma.com/) — 本地向量数据库
- [Streamlit](https://streamlit.io/) — Web 交互界面

## 快速开始

### 1. 安装依赖

需要 Python 3.10+。

```bash
pip install -r requirements.txt
```

### 2. 配置 API Key

本项目通过环境变量读取 DashScope API Key（[获取地址](https://dashscope.console.aliyun.com/)）：

```powershell
# Windows PowerShell
$env:DASHSCOPE_API_KEY = "你的 API Key"
```

```bash
# Linux / macOS
export DASHSCOPE_API_KEY="你的 API Key"
```

### 3. 启动应用

先启动上传页面，把 txt 知识文档传入向量库：

```bash
streamlit run app_file_upload.py
```

再启动聊天页面进行问答：

```bash
streamlit run app_mian.py
```

## 说明

- 对话历史和向量库都保存在本地目录（`history_storage/`、`chroma_db/`），程序重启后数据不会丢失。
- `chroma_db/` 和 `history_storage/` 中的内容是运行时数据，包含示例数据，可通过删除目录来重置。
