from typing import List, Dict
import httpx

from .config import OLLAMA_BASE_URL, OLLAMA_MODEL


async def ollama_chat(messages: List[Dict]) -> str:
    """
    Простой клиент для Ollama /api/chat.
    messages: список { "role": "system"|"user"|"assistant", "content": "..." }
    Возвращает текст ответа assistant.
    """
    url = f"{OLLAMA_BASE_URL}/api/chat"

    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()

    # Формат Ollama: { "message": { "role": "assistant", "content": "..." }, ... }
    return data["message"]["content"]
