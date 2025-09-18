from dataclasses import dataclass

@dataclass
class CategoryScoreDTO:
    category_name: str
    score: float
    mean: float | None = None
    deviation: float | None = None 