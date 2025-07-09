from pydantic import BaseModel
from typing import Dict
from .test_schema import TestSchema

class QuestionSchema(BaseModel):
    id: int
    test: TestSchema
    text: str
    scoring_rules: Dict

    class Config:
        orm_mode = True 