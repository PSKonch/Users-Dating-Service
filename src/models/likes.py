from datetime import datetime
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.db import Base

class LikesModel(Base):
    __tablename__ = "likes"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), index=True)
    liked_client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    client = relationship("ClientsModel", foreign_keys=[client_id], back_populates="likes_given")
    liked_client = relationship("ClientsModel", foreign_keys=[liked_client_id], back_populates="likes_received")