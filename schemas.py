from pydantic import BaseModel
from typing import Literal, Optional
from datetime import date
from uuid import UUID, uuid4
from enum import Enum


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
    env: EnvEnum # Enum сделать
    domain: DomainEnum # Enum сделать
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

class LockSchema(BaseModel):
    user: UUID
    locktime: Optional[float] = None # timestamp
    status: str # enum


