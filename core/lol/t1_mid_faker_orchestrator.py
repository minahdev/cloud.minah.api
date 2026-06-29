import os

import httpx

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
MODEL = "exaone3.5:2.4b"


class FakerOrchestrator:
    def __init__(self, system_prompt: str = ""):
        self.model = MODEL
        self.system_prompt = system_prompt
        self.history: list[dict] = []

    async def chat(self, user_message: str) -> str:
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.extend(self.history)
        messages.append({"role": "user", "content": user_message})

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                OLLAMA_URL,
                json={"model": self.model, "messages": messages, "stream": False},
            )
            response.raise_for_status()
            reply = response.json()["message"]["content"]

        self.history.append({"role": "user", "content": user_message})
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def reset(self):
        self.history.clear()
