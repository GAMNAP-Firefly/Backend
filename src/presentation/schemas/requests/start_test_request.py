from pydantic import BaseModel


class StartTestRequest(BaseModel):
    test_id: int
