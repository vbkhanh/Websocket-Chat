from pydantic import BaseModel
from datetime import datetime


class MessageUserOut(BaseModel):
    username: str

    class Config:
        from_attributes = True

class MessageOut(BaseModel):
    id: int
    content: str
    created_at: datetime
    user: MessageUserOut
     
    class Config:
        from_attributes = True