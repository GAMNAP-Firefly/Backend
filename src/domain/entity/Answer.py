from dataclasses import dataclass

from src.domain.entity.Question import Question
from src.domain.entity.Result import Result
from src.domain.entity.User import User
from src.domain.entity.Variant import Variant


@dataclass
class Answer:
    question: Question
    user: User
    variant: Variant
    result: Result

    def change_variant(self, variant_id):
        """Изменение варианта ответа"""
        self.variant_id = variant_id

