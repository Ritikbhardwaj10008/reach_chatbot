# app/main.py
from fastapi import FastAPI
from app.api import chat

app = FastAPI()
app.include_router(chat.router)

@app.get("/")
def root():
    return {"message": "RAG Chatbot API is up!"}
