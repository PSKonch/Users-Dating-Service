from sqlalchemy import select, update

from src.repositories.base import BaseRepository
from src.models.clients import ClientsModel
from src.repositories.mappers.clients import ClientsDataMapper

class ClientsRepository(BaseRepository):
    model = ClientsModel
    mapper = ClientsDataMapper

    async def update_avatar_path(self, client_id: int, new_avatar_path: str):
        update_stmt = (
            update(self.model)
            .where(self.model.id == client_id)
            .values(avatar_path=new_avatar_path)
        )
        await self.session.execute(update_stmt)
        await self.session.commit() 

    async def get_client_with_hashed_password(self, email: str):
        query = select(self.model).where(self.model.email == email)
        result = await self.session.execute(query)
        client = result.scalars().first()  # Получаем первый результат
        return client