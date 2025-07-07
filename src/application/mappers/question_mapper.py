from src.application.dto.QuestionDTO import QuestionDTO
from src.application.dto.VariantDTO import VariantDTO
from src.domain.entity.Question import Question
from src.domain.entity.Variant import Variant
from typing import List

def to_question_dto(question: Question, variants: List[Variant], index: int, total: int, answered: int) -> QuestionDTO:
    percent = round(answered / total * 100, 2) if total > 0 else 0.0
    variant_dtos = [VariantDTO(id=v.id, text=v.var_text) for v in variants]

    return QuestionDTO(
        id=question.id,
        text=question.text,
        index=index,
        total=total,
        progress_percent=percent,
        variants=variant_dtos
    ) 