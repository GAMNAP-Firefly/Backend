from pydantic import BaseModel


class GetUserTestStatisticsResponse(BaseModel):
    total_questions: int
    progress_percent: float

