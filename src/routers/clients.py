from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query

from src.utils.dependencies.db import DBDependency
from src.utils.dependencies.auth import ClientIdDependency
from src.utils.smtp import send_email

router = APIRouter(prefix="/api", tags=["Клиенты"])

@router.get("/list", summary="Получение списка клиентов")
async def get_clients(
    db: DBDependency,
    gender: Optional[str] = Query(None, description="Фильтр по полу"),
    first_name: Optional[str] = Query(None, description="Фильтр по имени"),
    second_name: Optional[str] = Query(None, description="Фильтр по фамилии")
):
    clients = await db.clients.get_filtered_clients(
        gender=gender,
        first_name=first_name,
        second_name=second_name,
    )
    return clients

@router.post("/api/clients/{id}/match")
async def match_user(
    id: int,
    current_user_id: ClientIdDependency,
    db: DBDependency,
):
    if await db.clients.check_existing_like(current_user_id, id):
        raise HTTPException(status_code=400, detail="Вы уже оценивали этого участника")

    await db.clients.add_like(current_user_id, id)

    if await db.clients.check_mutual_like(current_user_id, id):
        user_email = await db.clients.get_user_email(id)
        current_user_email = await db.clients.get_user_email(current_user_id)
        
        send_email(
            to_email=user_email,
            subject="Взаимная симпатия!",
            message=f"Вы понравились пользователю! Почта участника: {current_user_email}"
        )
        send_email(
            to_email=current_user_email,
            subject="Взаимная симпатия!",
            message=f"Вы понравились пользователю! Почта участника: {user_email}"
        )

        return {"message": "Взаимная симпатия!", "email": user_email}

    return {"message": "Оценка добавлена, но взаимной симпатии нет."}