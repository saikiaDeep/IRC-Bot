import chainlit as cl
import httpx

BACKEND_URL = "http://localhost:8000/chat"

@cl.on_message
async def main(message: cl.Message):
    # Send to FastAPI
    async with httpx.AsyncClient() as client:
        resp = await client.post(BACKEND_URL, json={"message": message.content})
        data = resp.json()
    
    await cl.Message(content=data["response"]).send()

