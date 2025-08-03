
# app/chat/memory.py
import json
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import SystemMessage

def get_memory(session_id, redis_client, mongo_collection, ttl):
    try:
        if redis_client.exists(session_id):
            raw = json.loads(redis_client.get(session_id))
        else:
            session = mongo_collection.find_one({"session_id": session_id},{"messages":{"$slice":-15}})
            raw = session["messages"] if session else []
            redis_client.set(session_id, json.dumps(raw), ex=ttl)
    except Exception as e:
        print(f"[Memory Load Error] {e}")
        raw = []

    memory = InMemoryChatMessageHistory()
    
    for msg in raw:
        role = msg.get("role")
        content = msg.get("content", "")
        if role == "user":
            memory.add_user_message(content)
        elif role == "ai":
            memory.add_ai_message(content)
        elif role == "system":
            memory.add_message(SystemMessage(content=content))
    
    #print(memory)
        
    return memory


def save_turn(session_id, user_msg, ai_msg, redis_client, mongo_collection, ttl):
    messages = [{"role": "user", "content": user_msg}, {"role": "ai", "content": ai_msg}]
    
    

    try:
        mongo_collection.update_one({"session_id": session_id}, {"$push": {"messages": {"$each": messages}}}, upsert=True)
        existing = json.loads(redis_client.get(session_id)) if redis_client.exists(session_id) else []
        #print("MongoDB insert successful.")
        
    except:
        existing = []
    existing.extend(messages)
    redis_client.set(session_id, json.dumps(existing), ex=ttl)