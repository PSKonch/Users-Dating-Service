from enum import Enum

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from src.db import Base

class ClientsModel(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(length=100))
    second_name: Mapped[str] = mapped_column(String(length=100))
    gender: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

    # Хранить медиафайлы в SQL базах данных не очень хорошо, насколько знаю
    avatar_path: Mapped[str]
