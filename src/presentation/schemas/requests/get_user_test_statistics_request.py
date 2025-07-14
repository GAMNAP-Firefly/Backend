from pydantic import BaseModel


class GetUserTestStatisticsRequest(BaseModel):
    result_id: int
