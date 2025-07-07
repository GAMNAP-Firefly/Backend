from abc import ABC, abstractmethod
from typing import List

from src.domain.entity.Question import Question


class QuestionRepository(ABC):
    @abstractmethod
    def add_question(self, question: Question) -> None:
        """Добавить вопрос"""
        pass

    @abstractmethod
    def get_question(self, question_id) -> Question:
        """Получить вопрос с id"""
        pass

    @abstractmethod
    def get_test_questions(self, test_id) -> List[Question]:
        """Получить вопросы в тесте с id"""
        pass

    @abstractmethod
    def delete_test_question(self, question_id) -> None:
        """Удалить вопрос с id"""
        pass

    @abstractmethod
    def edit_question(self, question_id: int, question: Question) -> None:
        """Изменить вопрос с id"""
        pass

    @abstractmethod
    def get_all_questions(self) -> List[Question]:
        """Получить все вопросы"""
        pass