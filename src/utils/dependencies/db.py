from typing import Annotated

from fastapi import Depends

from src.utils.db_manager import DBManager
from src.db import async_session_maker

async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db

DBDependency = Annotated[DBManager, Depends(get_db)]