from src.domain.entity.Answer import Answer

class SubmitAnswerUseCase:
    """
    Use case для сохранения ответа пользователя на вопрос.
    Использует паттерн "Upsert" (через метод save репозитория).
    """
    def __init__(self, answer_repo, question_repo, variant_repo, result_repo, user_repo):
        self.answer_repo = answer_repo
        self.question_repo = question_repo
        self.variant_repo = variant_repo
        self.result_repo = result_repo
        self.user_repo = user_repo

    async def execute(self, user_id: int, question_id: int, variant_id: int, result_id: int):
        """
        Выполняет use case.

        :param user_id: ID пользователя.
        :param question_id: ID вопроса, на который дается ответ.
        :param variant_id: ID выбранного варианта ответа.
        :param result_id: ID текущей сессии прохождения теста.
        """
        # 1. Получаем все необходимые сущности
        user = await self.user_repo.get_user(user_id)
        question = await self.question_repo.get_question(question_id)
        variant = await self.variant_repo.get_variant(variant_id)
        result = await self.result_repo.get_result_by_id(result_id)

        # 2. Создаем сущность Answer
        answer_to_save = Answer(
            question=question,
            user=user,
            variant=variant,
            result=result
        )

        # 3. Передаем ее в репозиторий, который сам решает, создать или обновить запись
        await self.answer_repo.save_answer(answer_to_save)