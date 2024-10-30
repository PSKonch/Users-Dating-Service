import os
from uuid import uuid4
from fastapi import HTTPException, Depends
from src.schemas.clients import ClientRequestAdd, ClientRequestLogin, ClientAdd, ClientUpdateData
from src.utils.image_processing import apply_watermark
from src.services.auth import AuthService
from src.utils.dependencies.db import DBDependency
from src.config import settings

class ClientService:
    def __init__(self, auth_service: AuthService = AuthService()):
        self.auth_service = auth_service


    async def register_user(self, data: ClientRequestAdd, avatar_file, db: DBDependency):
        avatar_filename = f"{uuid4().hex}_{avatar_file.filename}"
        avatar_path = os.path.join(settings.AVATAR_SAVE_PATH, avatar_filename)

        with open(avatar_path, "wb") as buffer:
            buffer.write(await avatar_file.read())

        watermark_image_path = "src/static/images/watermark.png"
        watermarked_path = await apply_watermark(avatar_path, watermark_image_path)
        if watermarked_path is None:
            raise HTTPException(status_code=500, detail="Ошибка наложения водяного знака")

        hashed_password = self.auth_service.hash_password(data.password)
        new_client_data = ClientAdd(
            first_name=data.first_name,
            second_name=data.second_name,
            gender=data.gender,
            email=data.email,
            hashed_password=hashed_password,
            avatar_path=watermarked_path
        )
        client = await db.clients.add(new_client_data)
        await db.commit()
        return client


    async def login_user(self, data: ClientRequestLogin, db: DBDependency):
        client = await db.clients.get_client_with_hashed_password(email=data.email)
        if not client or not self.auth_service.verify_password(data.password, client.hashed_password):
            raise HTTPException(status_code=401, detail="Неверные данные для входа")
        
        return self.auth_service.create_access_token({"client_id": client.id})


    async def get_current_client(self, client_id: int, db: DBDependency):
        client = await db.clients.get_one_or_none(id=client_id)
        if not client:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        return client


    async def update_client(self, client_id: int, data: ClientUpdateData, db: DBDependency):
        await db.clients.edit(data=data, id=client_id)
        await db.commit()
        updated_client = await db.clients.get_one_or_none(id=client_id)
        if not updated_client:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        return updated_client


    async def delete_client(self, client_id: int, db: DBDependency):
        await db.clients.delete(id=client_id)
        await db.commit()