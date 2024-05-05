from fastapi.routing import APIRouter

from schemas import AnswerPing

ping_router = APIRouter()


@ping_router.get("/ping", response_model=AnswerPing)
async def answer_ping() -> AnswerPing:
    return {"test": "new ok"}
