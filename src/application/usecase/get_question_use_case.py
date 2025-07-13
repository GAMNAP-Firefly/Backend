from typing import List

from src.application.dto.GetQuestionDTO import GetQuestionDTO, QuestionVariantDTO
from src.domain.entity.Question import Question
from src.domain.entity.Variant import Variant
from src.domain.repository.AnswerRepository import AnswerRepository
from src.domain.repository.QuestionRepository import QuestionRepository
from src.domain.repository.VariantRepository import VariantRepository


class GetQuestionUseCase:
    """
    Use case для получения следующего неотвеченного вопроса в тесте.
    """

    def __init__(self, answer_repo: AnswerRepository,
                 question_repo: QuestionRepository,
                 variant_repo: VariantRepository):
        self.answer_repo = answer_repo
        self.question_repo = question_repo
        self.variant_repo = variant_repo

    async def execute(self, question_id: int, user_id: int) -> GetQuestionDTO:
        """
        Выполняет use case.

        :param question_id: ID вопроса
        :param user_id: ID пользователя
        :return: DTO вопроса.
        """

        question: Question = await self.question_repo.get_question(question_id=question_id)
        if not question:
            raise ValueError("Вопроса с таким ID не существует")

        variants: List[Variant] = await self.variant_repo.get_variants_by_question_id(question_id=question_id)

        return GetQuestionDTO(
            id=question.id,
            text=question.text,
            variants=[QuestionVariantDTO(
                id=v.id,
                text=v.var_text,
                is_selected=True
                if len(await self.answer_repo.get_answers_by_variant_and_user(variant_id=v.id, user_id=user_id)) > 0
                else False
            ) for v in variants]
        )
