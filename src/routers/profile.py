from enum import Enum
from fastapi import APIRouter, Depends, Form, File, UploadFile
from pydantic import EmailStr
from src.utils.dependencies.db import DBDependency
from src.schemas.clients import ClientRequestAdd, ClientUpdateData
from src.services.clients import ClientService

client_service = ClientService()

router = APIRouter(prefix="/clients", tags=["Пользователи"])

class Gender(str, Enum):
    MALE = "M"
    FEMALE = "F"

@router.post("/create", summary="Регистрация нового пользователя")
async def register_user(
    db: DBDependency,
    first_name: str = Form(...),
    second_name: str = Form(...),
    gender: Gender = Form(...),
    email: EmailStr = Form(...),
    password: str = Form(...),
    avatar: UploadFile = File(...),
):
    data = ClientRequestAdd(
        first_name=first_name,
        second_name=second_name,
        gender=gender,
        email=email,
        password=password
    )
    client = await client_service.register_user(data, avatar, db)
    return {"status": "Регистрация успешна", "client_id": client.id}


@router.get("/me", summary="Получить текущего пользователя")
async def get_me(current_user=Depends(client_service.get_current_client)):
    return current_user


@router.patch("/me", summary="Обновить профиль пользователя")
async def update_user(
    data: ClientUpdateData,
    client_id=Depends(client_service.get_current_client),
    db = Depends(DBDependency)
):
    updated_client = await client_service.update_client(client_id, data, db)
    return updated_client


@router.delete("/me", summary="Удалить профиль пользователя")
async def delete_user(
    client_id=Depends(client_service.get_current_client),
    db = Depends(DBDependency)
):
    await client_service.delete_client(client_id, db)
    return {"status": "Пользователь успешно удален"}