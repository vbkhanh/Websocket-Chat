from pydantic import BaseModel

class GroupCreate(BaseModel):
    name: str

class GroupOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
