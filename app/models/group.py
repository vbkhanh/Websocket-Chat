from __future__ import annotations
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Group(Base):
    __tablename__ = "groups"

    name : Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    messages: Mapped[list["Message"]] = relationship("Message", back_populates="group", lazy="selectin")
