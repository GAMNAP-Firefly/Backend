from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .user_schema import UserSchema
from .test_schema import TestSchema

class ResultSchema(BaseModel):
    id: int
    user: UserSchema
    test: TestSchema
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    status: str
    link_token: Optional[str] = None
    interpretation: Optional[str] = None

    class Config:
        orm_mode = True 