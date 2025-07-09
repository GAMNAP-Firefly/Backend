from pydantic import BaseModel

class VariantSchema(BaseModel):
    id: int
    var_text: str

    class Config:
        orm_mode = True 