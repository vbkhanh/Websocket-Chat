from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base

class Group(Base):
    __tablename__ = "groups"

    name : Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
