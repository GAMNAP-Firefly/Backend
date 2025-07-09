from src.application.mappers.question_mapper import to_question_dto
from src.application.dto.QuestionDTO import QuestionDTO

class GetNextQuestionUseCase:
    """
    Use case для получения следующего неотвеченного вопроса в тесте.
    """
    def __init__(self, answer_repo, question_repo, variant_repo):
        self.answer_repo = answer_repo
        self.question_repo = question_repo
        self.variant_repo = variant_repo

    async def execute(self, user_id: int, test_id: int) -> QuestionDTO | None:
        """
        Выполняет use case.

        :param user_id: ID пользователя.
        :param test_id: ID теста.
        :return: DTO следующего вопроса или None, если все вопросы пройдены.
        """
        # 1. Получаем все вопросы теста и все ответы пользователя
        questions = await self.question_repo.get_test_questions(test_id)
        answered_answers = await self.answer_repo.get_user_answers(user_id)
        
        # 2. Создаем множество ID уже отвеченных вопросов для быстрого поиска
        answered_ids = {a.question.id for a in answered_answers}

        # 3. Ищем первый вопрос, ID которого нет в множестве отвеченных
        for index, question in enumerate(questions, start=1):
            if question.id not in answered_ids:
                variants = await self.variant_repo.get_variants_by_question_id(question.id)
                # Если нашли, маппим в DTO и возвращаем
                return to_question_dto(
                    question=question,
                    variants=variants,
                    index=index,
                    total=len(questions),
                    answered=len(answered_ids)
                )

        # 4. Если цикл завершился, значит все вопросы отвечены. Возвращаем None.
        return None 