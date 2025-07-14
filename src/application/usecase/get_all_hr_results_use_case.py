from src.application.dto.HRResultRowDTO import HRResultRowDTO


class GetAllHRResultsUseCase:
    """
    Use case для получения всех завершенных результатов для HR.
    Доступ защищен секретным ключом.
    """

    def __init__(self, result_repo):
        self.result_repo = result_repo

    def execute(self, access_key: str) -> list[HRResultRowDTO]:
        """
        Выполняет use case.

        :param access_key: Секретный ключ для доступа.
        :return: Список DTO с результатами для HR.
        :raises PermissionError: Если ключ доступа неверный.
        """
        # В реальном приложении ключ должен храниться в конфиге, а не хардкодиться
        if access_key != "HR_SECRET_KEY":
            raise PermissionError("Неверный ключ доступа")

        # 1. Получаем только завершенные результаты, фильтрация на стороне БД
        finished_results = self.result_repo.get_all_finished()

        # 2. Маппим в DTO для вывода
        return [
            HRResultRowDTO(
                test_name=r.test.name,
                start_time=r.start_time.isoformat(),
                end_time=r.end_time.isoformat() if r.end_time else '',
                link_token=r.link_token
            ) for r in finished_results if r.link_token
        ]
