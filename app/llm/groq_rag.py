# app/llm/groq_rag.py

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from config import settings
def build_rag_chain(get_memory):
    llm = ChatGroq(model="llama3-8b-8192", api_key=settings.GROQ_API_KEY,temperature=0.1)
    parser = StrOutputParser()

    from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

    prompt = ChatPromptTemplate.from_messages([
    ("system", 
    "You are a helpful and knowledgeable AI assistant for Reach CAD, a company specializing in advanced software solutions for pattern design, grading, marker planning, and apparel production systems. "
    "You must answer user questions strictly based on the retrieved company documentation and the current session's conversation history. "
    "Use prior messages in this session to maintain continuity and provide context-aware answers. "
    "If you do not have enough information to answer a question based on the available data, respond with: I'm sorry, I don't have that information at the moment. "
    "Always be professional, accurate, and user-friendly in your responses. Do not guess or provide information beyond the verified sources."
                                  ),
    
    MessagesPlaceholder(variable_name="history"),
    
    ("human", "{question}"),
    
    ("system", "Relevant context:\n{context}")
])

    chain = prompt | llm | parser

    return RunnableWithMessageHistory(
        chain,
        get_memory,
        input_messages_key="question",
        history_messages_key="history"
    )