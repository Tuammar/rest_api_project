from pydantic import BaseModel
from typing import Optional
from datetime import date
from uuid import UUID, uuid4
from enum import Enum

"""файл schemas.py содержит описание моделей,
необходимых для валидации данных при помощи pydantic"""

class AnswerPing(BaseModel):
    test: str

class DomainEnum(str, Enum):
    canary = "canary"
    regular = "regular"

class EnvEnum(str, Enum):
    prod = "prod"
    preprod = "preprod"
    stage = 'stage'

class UserSchema(BaseModel):
    user_id: UUID = uuid4()
    created_ad: date = date.today()
    login: str
    password: str
    project_id: UUID
    env: EnvEnum
    domain: DomainEnum
    locktime: float =  0.0

class AnswerSchema:
    title: str
    details: dict

class UserAuthorisationSchema(BaseModel):
    login: str 
    password: str

class LockAcquisitionSchema(BaseModel):
    user_id: UUID

class LockReleaseSchema(BaseModel):
    user_id: UUID

class LockEnum(str, Enum):
    user_not_found = "user not found"
    done = "done"
    error = "error"
    user_had_already_been_free = "user had already been free"
    user_had_already_been_locked = "user had already been locked"

class LockSchema(BaseModel):
    user: UUID
    locktime: Optional[float] = None
    status: LockEnum
