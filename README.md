# 🤖 ChatBot with RAG & RLHF — ChromaDB Edition

A **multi-user, AI-powered chatbot** built with **Streamlit**, **LangChain**, and **Azure OpenAI**. Upload your documents (PDF, DOCX, TXT, Images) and have intelligent, context-aware conversations — powered by **Retrieval-Augmented Generation (RAG)** with **ChromaDB** as the vector store and a built-in **RLHF feedback loop**.

![Screenshot](Screenshot%202026-03-23%20121919.png)

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🔐 **Multi-User Auth** | Register & login system with per-user data isolation, backed by ChromaDB |
| 📄 **Multi-Format Upload** | Supports **PDF**, **DOCX**, **TXT**, and **Images** (via OCR with Tesseract) |
| 🧠 **RAG Pipeline** | Semantic search over uploaded documents using Azure OpenAI Embeddings + ChromaDB |
| 🔄 **Dual-LLM Logic** | Primary model (`temperature=0.3`) for standard queries; creative model (`temperature=0.9`) for retries on negative feedback |
| 🛡️ **Intelligent Fallback** | If no answer is found in documents, seamlessly falls back to general AI — you're never left without an answer |
| 👍👎 **RLHF Feedback** | Thumbs up saves high-quality Q&A pairs to a feedback collection; thumbs down triggers a fresh response from the creative LLM |
| 💾 **Persistent Chat History** | All conversations are stored in ChromaDB, accessible across sessions per user |
| 🧹 **Session Management** | New chat, clear screen, delete all history, and logout — all from the sidebar |
| 🧑 **Name Recognition** | The bot detects "My name is ..." patterns and personalizes greetings |
| ⚡ **Rate-Limit Resilience** | Exponential backoff retry logic for Azure OpenAI embedding calls |

---

## 🏗️ Architecture

```
User ──▶ Streamlit UI ──▶ Auth (ChromaDB)
                │
                ▼
         Upload Documents
                │
                ▼
    ┌───────────────────────┐
    │  RAG Pipeline          │
    │  ┌─────────────────┐  │
    │  │ File Loader      │  │  ◀── PDF / DOCX / TXT / Image (OCR)
    │  └────────┬────────┘  │
    │           ▼           │
    │  ┌─────────────────┐  │
    │  │ Text Splitter    │  │  ◀── RecursiveCharacterTextSplitter (1000 / 100)
    │  └────────┬────────┘  │
    │           ▼           │
    │  ┌─────────────────┐  │
    │  │ Embeddings       │  │  ◀── Azure OpenAI Embeddings
    │  └────────┬────────┘  │
    │           ▼           │
    │  ┌─────────────────┐  │
    │  │ ChromaDB Store   │  │  ◀── Persistent Vector Store
    │  └─────────────────┘  │
    └───────────────────────┘
                │
                ▼
    ┌───────────────────────┐
    │  Query Processing      │
    │                       │
    │  Step 1: Doc Retrieval │ ──▶ Answer from documents
    │  Step 2: General AI    │ ──▶ Fallback if docs fail
    └───────────────────────┘
                │
                ▼
         RLHF Feedback (👍 / 👎)
```

---

## 📁 Project Structure

```
Chatgpt-Rag-Pdf-App-Chroma/
│
├── app.py                  # Main Streamlit application entry point
├── config.py               # Environment variable loading & configuration
├── db.py                   # ChromaDB client & collection initialization
├── requirements.txt        # Python dependencies
│
├── auth/                   # Authentication module
│   ├── login.py            # User login with credential verification
│   └── register.py         # New user registration
│
├── chat/                   # Chat engine & UI module
│   ├── chat_engine.py      # Dual-LLM initialization (normal + creative)
│   ├── chat_ui.py          # Sidebar rendering, file upload, chat history
│   └── history.py          # Cross-session conversation history retrieval
│
├── feedback/               # RLHF feedback module
│   └── rlhf.py             # 👍/👎 feedback handling & storage
│
├── rag/                    # RAG pipeline module
│   ├── file_loader.py      # Multi-format document loader (PDF, DOCX, TXT, OCR)
│   └── rag_pipeline.py     # Text splitting, embedding, vector store creation
│
├── utils/                  # Utility functions
│   └── session.py          # Streamlit session state initialization
│
└── temp/                   # Temporary file storage for uploads
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | [Streamlit](https://streamlit.io/) |
| **LLM Orchestration** | [LangChain](https://www.langchain.com/) |
| **LLM Provider** | [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service) (GPT models) |
| **Embeddings** | Azure OpenAI Embeddings |
| **Vector Database** | [ChromaDB](https://www.trychroma.com/) (persistent storage) |
| **Document Parsing** | PyPDFLoader, python-docx, Tesseract OCR |
| **Retry Logic** | [Tenacity](https://tenacity.readthedocs.io/) (exponential backoff) |

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.9+**
- **Azure OpenAI** account with deployed Chat & Embedding models
- **Tesseract OCR** installed ([download](https://github.com/tesseract-ocr/tesseract)) — required for image uploads

### 1. Clone the Repository

```bash
git clone https://github.com/Likithkumarr/Chatgpt-Rag-App-ChromaDB.git
cd Chatgpt-Rag-App
```

### 2. Create a Virtual Environment

```bash
python -m venv myenv
source myenv/bin/activate        # Linux / macOS
myenv\Scripts\activate           # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_CHAT_DEPLOYMENT=your-gpt-deployment-name
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=your-embedding-deployment-name
```

### 5. Run the Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## 🔄 How It Works

### Authentication Flow
1. **Register** — Create a new account (stored in ChromaDB `users` collection)
2. **Login** — Authenticate with username & password
3. Each user's chats, uploads, and feedback are isolated

### Chat Flow
1. **Upload Documents** — Drag & drop files in the sidebar (PDF, DOCX, TXT, or images)
2. **Ask Questions** — Type your query in the chat input
3. **Document Retrieval** — The system first searches your uploaded documents via semantic similarity
4. **Intelligent Fallback** — If no relevant answer is found in documents, falls back to general AI knowledge
5. **Feedback** — Use 👍 to save high-quality responses or 👎 to regenerate with the creative LLM

### Data Storage (ChromaDB Collections)

| Collection | Purpose |
|---|---|
| `users` | User credentials and profile data |
| `history` | Chat conversation history per user |
| `feedback` | Positively-rated Q&A pairs (RLHF data) |

---

## ⚙️ Configuration

Key configuration values in [config.py](config.py):

| Variable | Default | Description |
|---|---|---|
| `CHROMA_PATH` | `./chroma_db_v6` | Persistent storage path for ChromaDB |
| `CSV_FEEDBACK_FILE` | `good_responses.csv` | Legacy CSV feedback path (currently unused) |

---

## 📝 License

This project is open-source and available for educational and personal use.

---

## 🙋 Author

**Likith Kumar**
- GitHub: [@Likithkumarr](https://github.com/Likithkumarr)
