from fastapi import APIRouter, Response
from src.utils.dependencies.db import DBDependency
from src.schemas.clients import ClientRequestLogin
from src.services.clients import ClientService
from src.services.auth import AuthService

client_service = ClientService()
auth_service = AuthService()

router = APIRouter(tags=["Авторизация"])

@router.post("/auth/token", summary="Вход пользователя")
async def login_client(
    data: ClientRequestLogin,
    response: Response,
    db: DBDependency,
):
    access_token = await client_service.login_user(data, db)
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.delete("/auth/token", summary="Выход из системы")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "Вы успешно вышли из системы"}