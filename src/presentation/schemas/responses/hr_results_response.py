from pydantic import BaseModel
from typing import List

class HRResultRowResponse(BaseModel):
    test_name: str
    start_time: str
    end_time: str
    link_token: str

class HRResultsListResponse(BaseModel):
    results: List[HRResultRowResponse] 