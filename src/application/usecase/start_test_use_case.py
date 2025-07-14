from datetime import datetime
from typing import List

from src.application.dto.StartTestDTO import StartTestDTO
from src.domain.entity.Result import Result
from src.domain.entity.Test import Test
from src.domain.entity.User import User
from src.domain.repository.ResultRepository import ResultRepository
from src.domain.repository.TestRepository import TestRepository
from src.domain.repository.UserRepository import UserRepository


class StartTestUseCase:
    """
    Use case для начала нового теста.
    """

    def __init__(self, result_repo: ResultRepository,
                 user_repo: UserRepository,
                 test_repo: TestRepository):
        self.result_repo = result_repo
        self.user_repo = user_repo
        self.test_repo = test_repo

    async def execute(self, user_id: int, test_id: int) -> StartTestDTO:
        """
        Выполняет use case.

        :param result_id: ID результата связанного с пользователем и тестом.
        """
        user_results: List[Result] = await self.result_repo.get_user_result(user_id=user_id)
        result = next((r for r in user_results if r.test.id == test_id), None)
        if not result:
            user: User = await self.user_repo.get_user(user_id=user_id)
            test: Test = await self.test_repo.get_test(test_id=test_id)
            await self.result_repo.add_result(
                Result(
                    id=0,  # заглушка
                    user=user,
                    test=test,
                    start_time=None,
                    end_time=None,
                    status="in_progress"
                )
            )
            result: Result = await self.result_repo.get_user_test_result(user_id=user_id, test_id=test_id)
        return StartTestDTO(result_id=result.id)
