from typing import List

from src.application.dto.CandidateAnalysisDTO import CandidateAnalysisDTO
from src.application.dto.CategoryScoreDTO import CategoryScoreDTO
from src.application.service.scoring_service import ScoringService
from src.domain.entity.Answer import Answer
from src.domain.repository.AnswerRepository import AnswerRepository
from src.domain.repository.CategoryRepository import CategoryRepository
from src.domain.repository.QuestionRepository import QuestionRepository
from src.domain.repository.ResultRepository import ResultRepository
from src.domain.repository.TestRepository import TestRepository


class GetHRResultsByLinkUseCase:
    """
    Use case для получения результатов теста по ссылке для HR.
    Позволяет HR просматривать результаты кандидата по уникальному коду.
    """

    def __init__(self, result_repo: ResultRepository, answer_repo: AnswerRepository, question_repo: QuestionRepository,
                 category_repo: CategoryRepository, test_repo: TestRepository):
        self.result_repo: ResultRepository = result_repo
        self.answer_repo: AnswerRepository = answer_repo
        self.question_repo: QuestionRepository = question_repo
        self.category_repo: CategoryRepository = category_repo
        self.test_repo: TestRepository = test_repo

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
        answers: List[Answer] = await self.answer_repo.get_answers_by_result(result.id)
        for answer in answers:
            question = await self.question_repo.get_question(question_id=answer.question.id)
            answer.question.scoring_rules = question.scoring_rules
        scores = await ScoringService(self.category_repo).calculate_scores(answers)

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
