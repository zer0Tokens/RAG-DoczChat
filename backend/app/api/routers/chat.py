from fastapi import APIRouter, status, HTTPException
from app.api.schema.chat import ChatRequest, ChatResponse
from app.services.query_engine import get_query_engine

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/", status_code=status.HTTP_200_OK, response_model=ChatResponse)
def chat(body: ChatRequest):
    try:
        engine = get_query_engine()
        result = engine.query(body.query)
        return ChatResponse(answer=str(result))
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        ) from exc
