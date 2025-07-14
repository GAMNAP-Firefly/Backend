from pydantic import BaseModel


class GetResultResponse(BaseModel):
    result_id: int

