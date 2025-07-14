from pydantic import BaseModel


class FinishTestRequest(BaseModel):
    result_id: int
