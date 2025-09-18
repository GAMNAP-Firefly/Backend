from pydantic import BaseModel


class StartTestResponse(BaseModel):
    result_id: int
