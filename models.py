from pydantic import BaseModel
from typing import Literal
from datetime import date
from uuid import UUID, uuid4

class AnswerPing(BaseModel):
    test: str

class User(BaseModel):
    user_id: UUID = uuid4()
    created_ad: date = date.today()
    login: str
    password: str
    project_id: UUID
    env: Literal['prod', 'preprod', 'stage']
    domain: Literal['canary', 'regular']
    locktime: float =  0.0

class UserAuthorisation(BaseModel):
    login: str 
    password: str

class LockAcquisition(BaseModel):
    login: str
    password: str
    project_id: UUID

class LockRelease(BaseModel):
    login: str
    password: str
