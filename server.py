import asyncio

import ollama
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

async def ollama_stream(prompt: str):
    response = ollama.chat(
        model="Qwen3",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
        think=True,
    )

    for chunk in response:
        token = chunk["message"]["content"]
        if token:
            yield f"data: {token}\n\n"
            await asyncio.sleep(0)  # important for streaming

@app.post("/chat")
async def chat(payload: dict):
    return StreamingResponse(
        ollama_stream(payload["message"]),
        media_type="text/event-stream",
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)