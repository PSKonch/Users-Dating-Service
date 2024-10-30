from enum import Enum

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Float, String

from src.db import Base

class ClientsModel(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(length=100))
    second_name: Mapped[str] = mapped_column(String(length=100))
    gender: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    avatar_path: Mapped[str]
    latitude: Mapped[float] = mapped_column(Float, nullable=True)  # Широта
    longitude: Mapped[float] = mapped_column(Float, nullable=True)  # Долгота

    # Связь с таблицей LikesModel
    likes_given = relationship("LikesModel", foreign_keys="[LikesModel.client_id]", back_populates="client")
    likes_received = relationship("LikesModel", foreign_keys="[LikesModel.liked_client_id]", back_populates="liked_client")

