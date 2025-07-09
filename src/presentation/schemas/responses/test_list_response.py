from pydantic import BaseModel
from typing import List

class TestResponse(BaseModel):
    id: int
    name: str
    description: str

class TestListResponse(BaseModel):
    tests: List[TestResponse] 