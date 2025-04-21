from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    answer: str
