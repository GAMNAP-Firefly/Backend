from typing import List

from src.application.dto.GetQuestionListDTO import GetQuestionListDTO


class GetTestQuestionsUseCase:
    """
    Use case для получения всех вопросов в тесте.
    """

    def __init__(self, question_repo):
        self.question_repo = question_repo

    async def execute(self, test_id: int) -> List[GetQuestionListDTO] | None:
        """
        Выполняет use case.

        :param test_id: ID теста.
        :return: Список DTO вопросов в тесте.
        """
        questions = await self.question_repo.get_test_questions(test_id)
        questions_dto = []
        for question in questions:
            questions_dto.append(
                GetQuestionListDTO(
                    id=question.id
                )
            )

        # 2. Возвращаем список всех вопросов
        return questions_dto
