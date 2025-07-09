from pydantic import BaseModel

class CategorySchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True 