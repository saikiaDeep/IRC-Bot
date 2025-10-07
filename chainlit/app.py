import chainlit as cl

@cl.on_message
async def main(message: str):
    
    response = f"You said: {message}" 
    await cl.Message(content=response).send()
