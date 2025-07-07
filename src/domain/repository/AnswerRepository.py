from abc import ABC, abstractmethod
from typing import List

from src.domain.entity.Answer import Answer
from src.domain.entity.Question import Question
from src.domain.entity.Test import Test
from src.domain.entity.User import User


class AnswerRepository(ABC):
    @abstractmethod
    def add_answer(self, answer: Answer) -> None:
        """Добавить ответ"""
        pass

    @abstractmethod
    def get_answer(self, user_id: int , question_id: int) -> Answer:
        """Получить ответ по id пользователя и id вопроса"""
        pass

    @abstractmethod
    def get_user_answers(self, user_id: int) -> List[Answer]:
        """Получить все ответы пользователя с id"""
        pass

    @abstractmethod
    def get_question_answers(self, question_id: int) -> List[Answer]:
        """Получить все ответы на вопрос c id"""
        pass

    @abstractmethod
    def get_answers_by_result(self, result_id: int) -> List[Answer]:
        """Получить ответы из результата с id"""
        pass

    @abstractmethod
    def get_answers_by_variant(self, variant_id: int) -> List[Answer]:
        """Получить все ответы с вариантом с id"""
        pass

    @abstractmethod
    def delete_answer(self, question_id: int, user_id: int) -> None:
        """Удалить ответ пользователя с id на вопрос с id"""
        pass

    @abstractmethod
    def edit_answer(self,answer_id: int, answer: Answer) -> None:
        """Изменить вариант с id"""
        pass

    @abstractmethod
    def get_all_tests(self) -> List[Test]:
        """Получить все ответы"""
        pass