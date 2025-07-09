from pydantic import BaseModel

class TestSchema(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True 