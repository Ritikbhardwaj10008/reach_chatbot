# 🧠 Reach Technologies Chatbot

This is an intelligent RAG-based chatbot built with **FastAPI**, **LangChain**, **MongoDB**, and **Redis**. It supports session memory, streaming responses, and retrieval-augmented generation (RAG) using HuggingFace models. The chatbot is deployable locally and compatible with cloud platforms like Railway.

---

## 📌 Features

- 🔁 **Conversational Memory** (per session using Redis)
- 📄 **Document RAG** (PDF/Text/URL ingestion via Qdrant)
- 🤖 **LLM-powered replies** (via HuggingFace + LangChain)
- 🧠 **Session history** saved in MongoDB
- ⚡ **FastAPI backend** with Streamlit frontend
- ☁️ **Cloud-ready**: can be deployed with Docker or Railway

---

## 🧰 Tech Stack

- **Backend**: FastAPI, LangChain, Uvicorn
- **Vector Store**: Qdrant (via LangChain)
- **LLM**: HuggingFace Transformers (`sentence-transformers`, `Llama3`, etc.)
- **Frontend**: Streamlit (for chat UI)
- **Database**: MongoDB (session storage)
- **Memory**: Redis (conversation buffer)

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/reach-chatbot.git
cd reach-chatbot
2. Set Up Environment
Create a virtual environment:

bash
Copy
Edit
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate
Install dependencies:

bash
Copy
Edit
pip install --upgrade pip
pip install -r requirements.txt
3. Set Environment Variables
Create a .env file at the root:

env
Copy
Edit
MONGO_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net
REDIS_HOST=localhost
REDIS_PORT=6379
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
GROQ_API_KEY=your_groq_api_key
4. Run the Backend
bash
Copy
Edit
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
5. Run the Frontend (Streamlit)
bash
Copy
Edit
streamlit run frontend/app.py
🐳 Docker (Optional)
To build and run the Docker container:

bash
Copy
Edit
docker build -t reach-chatbot .
docker run -p 8000:8000 reach-chatbot
⚠️ Note: Final image size must be <1GB to deploy on Railway using Docker.

☁️ Deployment (Railway - Without Docker)
Remove Dockerfile from root.

Add a Procfile:

less
Copy
Edit
web: uvicorn app.main:app --host 0.0.0.0 --port 8000
Push project to GitHub.

Create Railway project → Deploy from GitHub.

Add environment variables.

Done!

📂 Project Structure
css
Copy
Edit
reach-chatbot/
├── app/
│   ├── api/
│   ├── chat/
│   ├── vectorstore/
│   └── main.py
├── frontend/
│   └── app.py
├── requirements.txt
├── Dockerfile
├── Procfile
└── README.md
📖 License
MIT License

🙋‍♂️ Contact
Developed by Reach Technologies AI Team
For issues or feature requests, open a GitHub issue.

yaml
Copy
Edit

---

Let me know if you'd like this adjusted to match your actual repo structure or team names.
