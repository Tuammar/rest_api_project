from fastapi.routing import APIRouter
from fastapi import Request

from models import User
from crud import CRUD

from pydantic import parse_obj_as


create_user_router = APIRouter()
crud_ex = CRUD()

async def create_user(request: Request) -> dict:
    params = dict(request.query_params)
    return {'login': params['login'], 'password': params['password'], 'project_id': params['project_id'], 'env': params['env'], 'domain': params['domain']}
    
# /create_user?env=stage&login=123&password=321&domain=regular&project_id=44a842a7-6675-41fd-b1e1-291896a2f9fb

@create_user_router.get("/create_user", response_model=User)
async def answer_create_user(request: Request) -> dict:
    new_user_data = parse_obj_as(User, await create_user(request))
    await crud_ex.create_user_db(new_user_data.user_id, new_user_data.created_ad,
                           new_user_data.login, new_user_data.password,
                           new_user_data.project_id, new_user_data.env, new_user_data.domain, new_user_data.locktime)
    return new_user_data