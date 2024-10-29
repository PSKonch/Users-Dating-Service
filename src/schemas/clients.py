from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr

class ClientAdd(BaseModel):
    first_name: str
    second_name: str
    gender: str
    email: EmailStr
    hashed_password: str
    avatar_path: str

class ClientRequestAdd(BaseModel):
    first_name: str
    second_name: str
    gender: str
    email: EmailStr
    password: str

class Client(ClientAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)

class ClientRequestLogin(BaseModel):
    email: EmailStr
    password: str

class ClientUpdateData(BaseModel):
    first_name: str | None = None
    second_name: str | None = None