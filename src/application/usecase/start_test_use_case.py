from datetime import datetime

from src.domain.entity.Result import Result
from src.domain.repository.ResultRepository import ResultRepository


class StartTestUseCase:
    """
    Use case для начала нового теста.
    """

    def __init__(self, result_repo: ResultRepository):
        self.result_repo = result_repo

    async def execute(self, result_id: int):
        """
        Выполняет use case.

        :param result_id: ID результата связанного с пользователем и тестом.
        """
        # 1. Получаем базовые сущности
        result: Result = await self.result_repo.get_result_by_id(result_id=result_id)
        result.start_time = datetime.now()
        result.status = "in_progress"
        await self.result_repo.edit_result_by_id(result.id, result)
