from datetime import datetime
from src.application.dto.StartTestResponseDTO import StartTestResponseDTO
from src.application.mappers.question_mapper import to_question_dto
from src.domain.entity.Result import Result

class StartTestUseCase:
    """
    Use case для начала нового теста.
    Создает сессию прохождения теста (Result) и возвращает первый вопрос.
    """
    def __init__(self, result_repo, question_repo, variant_repo, user_repo, test_repo, answer_repo):
        self.result_repo = result_repo
        self.question_repo = question_repo
        self.variant_repo = variant_repo
        self.user_repo = user_repo
        self.test_repo = test_repo
        self.answer_repo = answer_repo

    async def execute(self, user_id: int, test_id: int) -> StartTestResponseDTO:
        """
        Выполняет use case.

        :param user_id: ID пользователя, который начинает тест.
        :param test_id: ID теста, который нужно начать.
        :return: DTO с ID сессии (result_id) и первым вопросом.
        :raises Exception: Если у теста нет вопросов.
        """
        # 1. Получаем базовые сущности
        user = await self.user_repo.get_user(user_id)
        test = await self.test_repo.get_test(test_id)

        # 2. Создаем новую запись о прохождении теста (Result)
        result = Result(
            id=0,  # ID будет сгенерирован в репозитории при добавлении
            user=user,
            test=test,
            start_time=datetime.now(),
            end_time=None,
            status="in_progress"
        )
        await self.result_repo.add_result(result)

        # 3. Получаем первый вопрос теста
        questions = await self.question_repo.get_test_questions(test_id)
        if not questions:
            raise Exception("Test has no questions")

        question = questions[0]
        variants = await self.variant_repo.get_variants_by_question_id(question.id)
        
        # 4. Маппим данные в DTO для ответа.
        #    Количество отвеченных вопросов в начале теста всегда 0.
        question_dto = to_question_dto(
            question=question,
            variants=variants,
            index=1,
            total=len(questions),
            answered=0  # Оптимизация: убираем лишний запрос к БД
        )
        return StartTestResponseDTO(result_id=result.id, question=question_dto) 