from src.application.dto.QuestionDTO import QuestionDTO
from src.application.dto.VariantDTO import VariantDTO

class GetAnsweredQuestionUseCase:
    """
    Use case для получения уже отвеченного вопроса.
    Это позволяет пользователю вернуться назад и посмотреть свой ответ.
    """
    def __init__(self, answer_repo, question_repo, variant_repo):
        self.answer_repo = answer_repo
        self.question_repo = question_repo
        self.variant_repo = variant_repo

    async def execute(self, user_id: int, test_id: int, question_id: int) -> QuestionDTO:
        """
        Выполняет use case.

        :param user_id: ID пользователя.
        :param test_id: ID теста (нужен для расчета прогресса).
        :param question_id: ID вопроса, который нужно получить.
        :return: DTO вопроса с отмеченным вариантом ответа.
        :raises Exception: Если вопрос с таким ID не найден в тесте.
        """
        # 1. Получаем все вопросы и все ответы для теста одним запросом каждый
        all_questions = await self.question_repo.get_test_questions(test_id)
        all_answers = await self.answer_repo.get_user_answers_for_test(user_id, test_id)

        # 2. Находим нужный вопрос и его индекс в памяти
        question_tuple = next(((i, q) for i, q in enumerate(all_questions, 1) if q.id == question_id), None)
        if question_tuple is None:
            raise Exception("Question not found in this test")
        index, question = question_tuple
        
        # 3. Находим ответ на этот вопрос в памяти
        answer = next((a for a in all_answers if a.question.id == question_id), None)
        selected_variant_id = answer.variant.id if answer else None

        # 4. Получаем варианты для вопроса
        variants = await self.variant_repo.get_variants_by_question_id(question_id)
        variant_dtos = [
            VariantDTO(
                id=v.id,
                text=v.var_text,
                is_selected=(v.id == selected_variant_id)
            )
            for v in variants
        ]

        # 5. Собираем финальный DTO вопроса
        total = len(all_questions)
        answered_count = len(all_answers)
        percent = round(answered_count / total * 100, 2) if total else 0.0

        return QuestionDTO(
            id=question.id,
            text=question.text,
            index=index,
            total=total,
            progress_percent=percent,
            variants=variant_dtos
        ) 