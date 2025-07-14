from pydantic import BaseModel


class StartTestRequest(BaseModel):
    result_id: int
