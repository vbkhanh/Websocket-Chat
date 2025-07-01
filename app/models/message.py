from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class Message(Base):
    __tablename__ = "messages"

    content : Mapped[str] = mapped_column(Text, nullable=False)

    group_id : Mapped[int] = mapped_column(Integer, ForeignKey("groups.id"))
    user_id : Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
