from dataclasses import dataclass

from src.domain.entity.Test import Test


@dataclass
class Question:
    id: int
    test: Test
    text: str
    scoring_rules: dict

    def change_test(self, test_id):
        """Изменить тест к которому относится вопрос"""
        self.test_id = test_id

    def change_text(self, text):
        """Изменить текст вопроса"""
        self.text = text

    def change_scoring_rules(self, scoring_rules):
        """Изменить правило начисления баллов"""
        self.scoring_rules = scoring_rules

