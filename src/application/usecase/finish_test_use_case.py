import uuid
from datetime import datetime
from src.application.service.scoring_service import ScoringService
from src.application.dto.CategoryScoreDTO import CategoryScoreDTO

class FinishTestUseCase:
    """
    Use case для завершения теста.
    Подсчитывает результаты, генерирует токен-ссылку для HR и обновляет статус сессии.
    """
    def __init__(self, result_repo, answer_repo, category_repo):
        self.result_repo = result_repo
        self.answer_repo = answer_repo
        self.category_repo = category_repo

    async def execute(self, result_id: int) -> list[CategoryScoreDTO]:
        """
        Выполняет use case.

        :param result_id: ID сессии (Result), которую нужно завершить.
        :return: Список DTO с результатами по каждой категории.
        """
        # 1. Получаем все необходимые данные из репозиториев
        result = await self.result_repo.get_result_by_id(result_id)
        answers = await self.answer_repo.get_answers_by_result(result_id)
        
        # 2. Выполняем бизнес-логику (подсчет очков)
        scores = ScoringService().calculate_scores(answers)

        # 3. Собираем данные для DTO (имена категорий)
        category_ids = list(scores.keys())
        categories = await self.category_repo.get_categories_by_ids(category_ids)
        category_map = {c.id: c.name for c in categories}

        # 4. Обновляем и сохраняем сущность со всеми изменениями
        result.status = "finished"
        result.end_time = datetime.now()
        result.assign_link_token(uuid.uuid4().hex[:8])

        # Здесь будет место вызова LLM
        # Анализ генерируется на основе `scores`, передаётся в GPT
        result.set_interpretation("[Анализ будет добавлен позже]")

        await self.result_repo.edit_result_by_id(result_id, result)
        
        # 5. Возвращаем готовый DTO
        return [
            CategoryScoreDTO(
                category_name=category_map.get(cid, "Unknown Category"),
                score=score
            ) for cid, score in scores.items()
        ] 