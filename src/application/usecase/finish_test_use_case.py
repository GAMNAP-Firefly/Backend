import uuid
from datetime import datetime
from typing import List

from src.application.dto.CandidateAnalysisDTO import CandidateAnalysisDTO
from src.application.dto.CategoryScoreDTO import CategoryScoreDTO
from src.application.dto.HRShareLinkDTO import HRShareLinkDTO
from src.application.service.ai_service import AiService, Model, Prompt
from src.application.service.scoring_service import ScoringService
from src.domain.entity.Answer import Answer
from src.domain.entity.Result import Result
from src.domain.repository.AnswerRepository import AnswerRepository
from src.domain.repository.CategoryRepository import CategoryRepository
from src.domain.repository.QuestionRepository import QuestionRepository
from src.domain.repository.ResultRepository import ResultRepository
from src.domain.repository.TestRepository import TestRepository


class FinishTestUseCase:
    """
    Use case для завершения теста.
    Подсчитывает результаты, генерирует токен-ссылку для HR и обновляет статус сессии.
    """

    def __init__(self, result_repo: ResultRepository,
                 answer_repo: AnswerRepository,
                 category_repo: CategoryRepository,
                 question_repo: QuestionRepository,
                 test_repo: TestRepository):
        self.result_repo = result_repo
        self.answer_repo = answer_repo
        self.category_repo = category_repo
        self.question_repo = question_repo
        self.test_repo = test_repo
        self.ai_service = AiService(model=Model.GEMINI_FLASH)


    async def execute(self, result_id: int) -> tuple[CandidateAnalysisDTO, list[CategoryScoreDTO], HRShareLinkDTO]:
        """
        Выполняет use case.

        :param result_id: ID сессии (Result), которую нужно завершить.
        :return: Кортеж (список DTO с результатами по каждой категории, DTO ссылки для HR).
        """
        # 1. Получаем все необходимые данные из репозиториев
        result: Result = await self.result_repo.get_result_by_id(result_id)
        answers: List[Answer] = await self.answer_repo.get_answers_by_result(result_id)
        for answer in answers:
            question = await self.question_repo.get_question(question_id=answer.question.id)
            answer.question.scoring_rules = question.scoring_rules

        # 2. Выполняем бизнес-логику (подсчет очков)
        scores = await ScoringService(self.category_repo).calculate_scores(answers)
        # 3. Собираем данные для DTO (имена категорий)
        category_ids = list(scores.keys())
        categories = await self.category_repo.get_categories_by_ids(category_ids)
        category_map = {c.id: c.name for c in categories}

        # 4. Генерируем код для HR
        share_code = uuid.uuid4().hex[:8].upper()

        # 5. Обновляем и сохраняем сущность со всеми изменениями
        result.status = "finished"
        result.end_time = datetime.now()
        result.assign_link_token(share_code)

        ai_response = self.ai_service.generate(category_map, scores, Prompt.MMPI)

        result.set_interpretation(ai_response)

        await self.result_repo.edit_result_by_id(result_id, result)

        # 6. Создаем DTO для ссылки HR
        hr_share_link = HRShareLinkDTO(share_code=share_code)

        # 7. Возвращаем готовые DTO
        category_scores = [
            CategoryScoreDTO(
                category_name=category_map.get(cid, "Unknown Category"),
                score=score
            ) for cid, score in scores.items()
        ]
        duration_minutes = (result.end_time - result.start_time).total_seconds() / 60
        test = await self.test_repo.get_test(result.test.id)

        candidate_analysis = CandidateAnalysisDTO(
            test_name=test.name,
            start_time=result.start_time.isoformat(),
            end_time=result.end_time.isoformat(),
            duration_minutes=duration_minutes,
            interpretation=result.interpretation or "Анализ недоступен"
        )

        return candidate_analysis, category_scores, hr_share_link
