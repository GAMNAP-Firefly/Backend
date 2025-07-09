from src.application.dto.TestDTO import TestDTO

class GetAllTestsUseCase:
    """
    Use case для получения списка всех доступных тестов.
    """
    def __init__(self, test_repo):
        """
        Инициализатор use case.

        :param test_repo: Репозиторий для работы с тестами.
        """
        self.test_repo = test_repo

    async def execute(self) -> list[TestDTO]:
        """
        Выполняет use case.

        :return: Список DTO с информацией о тестах.
        """
        # 1. Получаем все сущности тестов из репозитория
        tests = await self.test_repo.get_all_tests()

        # 2. Маппим каждую сущность в TestDTO, чтобы отдать наружу только нужные данные
        return [TestDTO(id=t.id, name=t.name, description=t.description) for t in tests] 