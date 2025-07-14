from dataclasses import dataclass


@dataclass
class GetUserTestStatisticsDTO:
    total_questions: int
    progress_percent: float
