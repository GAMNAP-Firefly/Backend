from typing import List, Optional

from pydantic import BaseModel


class TestResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]


class TestListResponse(BaseModel):
    tests: List[TestResponse]
