from datetime import datetime
from typing import List

from src.application.dto.GetResultDTO import GetResultDTO
from src.application.dto.GetUserTestStatisticsDTO import GetUserTestStatisticsDTO
from src.domain.entity.Answer import Answer
from src.domain.entity.Question import Question
from src.domain.entity.Result import Result
from src.domain.entity.Test import Test
from src.domain.entity.User import User
from src.domain.repository.AnswerRepository import AnswerRepository
from src.domain.repository.QuestionRepository import QuestionRepository
from src.domain.repository.ResultRepository import ResultRepository
from src.domain.repository.TestRepository import TestRepository
from src.domain.repository.UserRepository import UserRepository


class GetUserTestStatisticsUseCase:
    """
    Use case для получения статистики пользователя по прохождению теста.
    """

    def __init__(self, result_repo: ResultRepository,
                 question_repo: QuestionRepository,
                 answer_repo: AnswerRepository):
        self.result_repo = result_repo
        self.question_repo = question_repo
        self.answer_repo = answer_repo

    async def execute(self, result_id: int) -> GetUserTestStatisticsDTO:
        """
        Выполняет use case.

        :param result_id: ID результата
        :return: DTO результата.
        """
        result: Result = await self.result_repo.get_result_by_id(result_id=result_id)
        all_test_questions: List[Question] = await self.question_repo.get_test_questions(test_id=result.test.id)
        answered_questions: List[Answer] = await self.answer_repo.get_user_answers_for_test(user_id=result.user.id,
                                                                                            test_id=result.test.id)
        return GetUserTestStatisticsDTO(total_questions=len(all_test_questions),
                                        progress_percent=float(len(answered_questions) / len(all_test_questions)))
