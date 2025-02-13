from math import atan2, cos, radians, sin, sqrt
from sqlalchemy import and_, func, select, update

from src.models.likes import LikesModel
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
    
    async def get_filtered_clients(
        self, 
        gender: str | None = None, 
        first_name: str | None = None, 
        second_name: str | None = None, 
        current_latitude: float | None = None,
        current_longitude: float | None = None,
        max_distance: float | None = None
    ) -> list:
        
        query = select(self.model)
        
        # Фильтры по полу, имени, фамилии
        if gender:
            query = query.filter(self.model.gender == gender)
        if first_name:
            query = query.filter(func.lower(self.model.first_name).contains(first_name.strip().lower()))
        if second_name:
            query = query.filter(func.lower(self.model.second_name).contains(second_name.strip().lower()))

        result = await self.session.execute(query)
        clients = result.scalars().all()

        # Дополнительная фильтрация по расстоянию
        if (current_latitude is not None) and (current_longitude is not None) and (max_distance is not None):
            clients = [
                client for client in clients 
                if (client.latitude is not None) and (client.longitude is not None) and
                self.calculate_distance(
                    current_latitude, current_longitude, client.latitude, client.longitude
                ) <= max_distance
            ]

        return [self.mapper.map_to_domain_entity(client) for client in clients]

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        R = 6371  # Радиус Земли в километрах
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c
    
    async def get_user_email(self, user_id: int) -> str:
        stmt = select(ClientsModel.email).filter(ClientsModel.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def check_existing_like(self, user_id: int, liked_user_id: int) -> bool:
        stmt = select(LikesModel).filter(
            and_(
                LikesModel.client_id == user_id,
                LikesModel.liked_client_id == liked_user_id
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar() is not None

    async def add_like(self, user_id: int, liked_user_id: int):
        new_like = LikesModel(client_id=user_id, liked_client_id=liked_user_id)
        self.session.add(new_like)
        await self.session.commit()

    async def check_mutual_like(self, user_id: int, liked_user_id: int) -> bool:
        stmt = select(LikesModel).filter(
            and_(
                LikesModel.client_id == liked_user_id,
                LikesModel.liked_client_id == user_id
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar() is not None