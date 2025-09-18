from dataclasses import dataclass
from src.application.dto.QuestionDTO import QuestionDTO

@dataclass
class StartTestResponseDTO:
    result_id: int
    question: QuestionDTO 