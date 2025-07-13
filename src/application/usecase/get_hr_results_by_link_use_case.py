from datetime import datetime
from src.application.dto.CandidateAnalysisDTO import CandidateAnalysisDTO
from src.application.dto.CategoryScoreDTO import CategoryScoreDTO

class GetHRResultsByLinkUseCase:
    """
    Use case для получения результатов теста по ссылке для HR.
    Позволяет HR просматривать результаты кандидата по уникальному коду.
    """
    def __init__(self, result_repo, answer_repo, category_repo, test_repo):
        self.result_repo = result_repo
        self.answer_repo = answer_repo
        self.category_repo = category_repo
        self.test_repo = test_repo

    async def execute(self, share_code: str) -> tuple[CandidateAnalysisDTO, list[CategoryScoreDTO]]:
        """
        Выполняет use case.

        :param share_code: Уникальный код для доступа к результатам.
        :return: Кортеж (DTO с анализом кандидата, список DTO с результатами по категориям).
        """
        # 1. Получаем результат по коду ссылки
        result = await self.result_repo.get_result_by_token(share_code)
        if not result:
            raise ValueError("Результат не найден или ссылка недействительна")
        
        # 2. Проверяем, что тест завершен
        if result.status != "finished":
            raise ValueError("Тест еще не завершен")
        
        # 3. Получаем данные теста
        test_id = await self.result_repo.get_test_id_by_token(share_code)
        test = await self.test_repo.get_test(test_id)
        
        # 4. Получаем ответы и рассчитываем баллы
        answers = await self.answer_repo.get_answers_by_result(result.id)
        from src.application.service.scoring_service import ScoringService
        scores = ScoringService().calculate_scores(answers)
        
        # 5. Получаем названия категорий
        category_ids = list(scores.keys())
        categories = await self.category_repo.get_categories_by_ids(category_ids)
        category_map = {c.id: c.name for c in categories}
        
        # 6. Создаем DTO анализа кандидата
        duration_minutes = (result.end_time - result.start_time).total_seconds() / 60
        
        candidate_analysis = CandidateAnalysisDTO(
            test_name=test.name,
            start_time=result.start_time.isoformat(),
            end_time=result.end_time.isoformat(),
            duration_minutes=duration_minutes,
            interpretation=result.interpretation or "Анализ недоступен"
        )
        
        # 7. Создаем DTO результатов по категориям
        category_scores = [
            CategoryScoreDTO(
                category_name=category_map.get(cid, "Unknown Category"),
                score=score
            ) for cid, score in scores.items()
        ]
        
        return candidate_analysis, category_scores 