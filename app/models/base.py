from sqlalchemy.sql import func
from sqlalchemy import DateTime, Integer
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

from app.db import BaseModel

class Base(BaseModel):
    __abstract__ = True

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at : Mapped[datetime ] = mapped_column(DateTime(timezone=True), server_default=func.now())
