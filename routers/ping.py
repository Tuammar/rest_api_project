from fastapi.routing import APIRouter

from models import AnswerPing

ping_router = APIRouter()

async def ping():
    return {'test': 'ok'}

@ping_router.get("/ping", response_model=AnswerPing)
async def answer_ping():
    return await ping()