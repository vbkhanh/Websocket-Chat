from __future__ import annotations
from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Message(Base):
    __tablename__ = "messages"

    content : Mapped[str] = mapped_column(Text, nullable=False)
    group_id : Mapped[int] = mapped_column(Integer, ForeignKey("groups.id"))
    user_id : Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    group : Mapped["Group"] = relationship("Group", back_populates="messages", lazy="subquery")
    user : Mapped["User"] = relationship("User", back_populates="messages", lazy="subquery")
    