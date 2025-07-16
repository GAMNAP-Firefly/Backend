from src.domain.entity.Category import Category
from src.domain.repository.CategoryRepository import CategoryRepository


class ScoringService:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository: CategoryRepository = category_repository

    async def _raw_to_t_scores(self, scale_name: str, score: int, mean: float, deviation: float) -> float:
        if mean is None: mean = 0
        if deviation is None: deviation = 0
        return 50 + 10 * (score - mean) / deviation

    async def calculate_scores(self, answers: list) -> dict:
        category_scores = {}
        for answer in answers:
            rules = answer.question.scoring_rules
            variant_id = str(answer.variant.id)
            if variant_id in rules:
                for category_id, score in rules[variant_id].items():
                    cid = int(category_id)
                    category_scores[cid] = category_scores.get(cid, 0) + score

        for category_id, score in category_scores.items():
            category: Category = await self.category_repository.get_category(category_id=category_id)
            scale_name = category.name
            mean = category.mean
            deviation = category.deviation
            category_scores[category_id] = await self._raw_to_t_scores(scale_name=scale_name,
                                                                       score=score,
                                                                       mean=mean,
                                                                       deviation=deviation)

        return category_scores
