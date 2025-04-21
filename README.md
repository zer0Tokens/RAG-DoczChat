# 🧠 RAG-DoczChat

Upload your documents and chat with them using AI — in seconds.  
Built for developers, researchers, and teams who want lightning-fast insights from their own files.

---

## 🚀 Tech Stack

This project is powered by a modern and scalable AI-first fullstack architecture:

| Layer     | Tech Used                       |
|-----------|----------------------------------|
| 🧩 Frontend  | [React](https://react.dev) + [Vite](https://vitejs.dev) |
| ⚙️ Backend   | [FastAPI](https://fastapi.tiangolo.com) – blazing fast, Pythonic APIs |
| 🧠 AI Engine | [LlamaIndex](https://www.llamaindex.ai/) with [OpenAI](https://platform.openai.com) models |
| 💾 Vector DB | `sqlite_vec` – lightweight, local vector search (no Pinecone needed) |
| 📄 File Support | `.pdf` and `.docx` ingestion with cleaning and embedding |

---

### 🧘 No External Vector DB Required

> 💡 RAG-DoczChat uses a **fully local vector store** via [`sqlite_vec`](https://github.com/asg017/sqlite-vss).  
> That means **no Pinecone, no Chroma, no cloud database** — all your document embeddings are stored and queried directly in SQLite.

Perfect for privacy-focused workflows, testing, and offline setups.

---

## ✨ Features

- 📄 Upload PDF or DOCX files
- 🔍 Vectorize and index documents with OpenAI Embeddings
- 💬 Ask questions and receive contextual answers via LLMs
- ♻️ Automatic document cleaning, chunking, and semantic splitting
- ⚡ Fast local semantic search — no internet database needed
