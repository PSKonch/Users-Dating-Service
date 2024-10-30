from fastapi import APIRouter, Depends, Query
from typing import Optional, List
from src.utils.dependencies.db import DBDependency

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