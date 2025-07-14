class ScoringService:
    def calculate_scores(self, answers: list) -> dict:
        category_scores = {}
        for answer in answers:
            rules = answer.question.scoring_rules
            variant_id = str(answer.variant.id)
            if variant_id in rules:
                for category_id, score in rules[variant_id].items():
                    cid = int(category_id)
                    category_scores[cid] = category_scores.get(cid, 0) + score

        for category_id, score in category_scores.items():
            category_scores[category_id] = 50 + 10 * (score - 50) / 10

        return category_scores
