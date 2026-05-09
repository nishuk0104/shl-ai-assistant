from fastapi import FastAPI

from app.models import ChatRequest
from app.recommendation_engine import process_chat

app = FastAPI()


@app.get("/health")
def health():

    return {
        "status": "ok"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    response = process_chat(
        [msg.dict() for msg in request.messages]
    )

    return response