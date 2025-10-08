from fastapi import FastAPI
from pydantic import BaseModel
#from rag_service import query_rag
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/chat")
def chat(request: ChatRequest):
    response_text = "query_rag(request.message)"
    return {"response": response_text}
