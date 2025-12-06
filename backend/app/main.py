from fastapi import FastAPI
from pydantic import BaseModel

from .ollama_client import ollama_chat

app = FastAPI(
    title="ChatCourseFactory Backend",
    description="FastAPI backend для ChatCourseFactory: AI, курсы, TON, Telegram.",
)


class ChatRequest(BaseModel):
    role: str = "teacher"
    prompt: str


class ChatResponse(BaseModel):
    reply: str


@app.get("/health")
async def health():
    return {"status": "ok", "service": "backend"}


@app.post("/ai/chat", response_model=ChatResponse)
async def ai_chat(req: ChatRequest):
    """
    Базовая точка входа для общения с Ollama.
    Дальше сюда будем заворачивать логику AI-Teacher, AI-Sales и т.д.
    """

    system_prompt_map = {
        "teacher": "You are AI-Teacher for ChatCourseFactory. You explain concepts clearly and step-by-step.",
        "sales": "You are AI-Sales for ChatCourseFactory. You help users decide which course to buy.",
        "support": "You are AI-Support for ChatCourseFactory. You answer questions briefly and clearly.",
        "methodologist": "You are AI-Methodologist for ChatCourseFactory. You design course structures.",
        "content": "You are AI-Content creator for ChatCourseFactory. You write concise, engaging texts.",
        "finance": "You are AI-Finance for ChatCourseFactory. You explain payments and TON usage.",
        "marketplace": "You are AI-Marketplace agent for ChatCourseFactory. You recommend suitable courses.",
        "ceo": "You are AI-CEO for ChatCourseFactory. You think strategically about the project.",
    }

    role = req.role.lower()
    system_text = system_prompt_map.get(role, system_prompt_map["teacher"])

    messages = [
        {"role": "system", "content": system_text},
        {"role": "user", "content": req.prompt},
    ]

    reply = await ollama_chat(messages)

    return ChatResponse(reply=reply)
