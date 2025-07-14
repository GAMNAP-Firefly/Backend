from pydantic import BaseModel


class GetUserTestStatisticsResponse(BaseModel):
    total: int
    progress_percent: float

