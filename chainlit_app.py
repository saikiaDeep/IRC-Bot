import chainlit as cl
import httpx

BACKEND_URL = "http://localhost:8001/chat"

@cl.on_chat_start
async def start():
    await cl.Message(
        content="""
👋 Welcome to **IRC Bot**!

I am your AI assistant with complete knowledge of the **Indian Roads Congress (IRC)**.  
Type your question below to get started! 
"""
        
    ).send()



@cl.on_message
async def main(message: cl.Message):
    # Send to FastAPI
    async with httpx.AsyncClient() as client:
        resp = await client.post(BACKEND_URL, json={"message": message.content})
        data = resp.json()
    
    await cl.Message(content=data["response"]).send()
