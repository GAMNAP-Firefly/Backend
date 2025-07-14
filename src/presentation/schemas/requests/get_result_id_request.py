from pydantic import BaseModel


class GetResultRequest(BaseModel):
    test_id: int
