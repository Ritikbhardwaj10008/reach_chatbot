from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from pymongo.errors import PyMongoError
from pymongo import MongoClient
import redis
from urllib.parse import urlparse

from app.vectorstore.qdrant_store import retriever
from app.chat.memory import get_memory, save_turn
from app.llm.groq_rag import build_rag_chain
from config import settings

router = APIRouter()

# MongoDB setup
mongo_collection = MongoClient(settings.MONGO_URI)[settings.MONGO_DB_NAME].sessions

# Redis setup (using URL)
parsed = urlparse(settings.REDIS_URL)
redis_client = redis.StrictRedis(
    host=parsed.hostname,
    port=parsed.port,
    password=parsed.password,
    ssl=True,
    decode_responses=True
)

# Memory setup
def memory_provider(session_id: str):
    return get_memory(session_id, redis_client, mongo_collection, settings.REDIS_TTL)

# Build the RAG chain
rag_chain = build_rag_chain(memory_provider)

# Pydantic model for input validation
class ChatRequest(BaseModel):
    query: str
    session_id: str

# ========== 1. POST /chat ==========
@router.post("/chat")
def chat(request_data: ChatRequest):
    query = request_data.query
    session_id = request_data.session_id

    context_docs = retriever.get_relevant_documents(query)
    context = "\n\n".join([doc.page_content for doc in context_docs])

    result = rag_chain.invoke(
        {"question": query, "context": context},
        config={"configurable": {"session_id": session_id}}
    )

    save_turn(session_id, query, result, redis_client, mongo_collection, settings.REDIS_TTL)
    return {"response": result}

# ========== 2. GET /sessions ==========
@router.get("/sessions")
def get_all_sessions() -> List[Dict[str, str]]:
    try:
        sessions = mongo_collection.find({}, {"_id": 0, "session_id": 1, "messages": 1}).sort("created_at", -1)
        session_list = []
        for session in sessions:
            first_question = ""
            for msg in session.get("messages", []):
                if msg.get("role") == "user":
                    first_question = msg.get("content", "")[:50]  # first 50 characters
                    break
            session_list.append({
                "session_id": session["session_id"],
                "title": first_question or session["session_id"][:8],  # fallback title
            })
        return session_list
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"MongoDB error: {str(e)}")

# ========== 3. GET /sessions/{session_id} ==========
@router.get("/sessions/{session_id}")
def get_session_history(session_id: str) -> List[Dict[str, str]]:
    try:
        session = mongo_collection.find_one({"session_id": session_id})
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return session.get("messages", [])
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"MongoDB error: {str(e)}")

@router.post("/sessions/{session_id}/title")
def set_session_title(session_id: str, body: Dict[str, str]):
    try:
        title = body.get("title", "").strip()
        if not title:
            raise HTTPException(status_code=400, detail="Title is required")
        result = mongo_collection.update_one(
            {"session_id": session_id},
            {"$set": {"title": title}},
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Session not found")
        return {"message": "Title updated"}
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"MongoDB error: {str(e)}")
