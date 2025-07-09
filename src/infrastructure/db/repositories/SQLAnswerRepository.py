from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entity.Test import Test
from src.domain.repository.AnswerRepository import AnswerRepository
from src.domain.entity.Answer import Answer
from src.domain.entity.Question import Question
from src.domain.entity.User import User
from src.domain.entity.Variant import Variant
from src.domain.entity.Result import Result
from src.infrastructure.db.models.answer_model import AnswerModel
from sqlalchemy import select
from typing import List
from src.infrastructure.db.models.result_model import ResultModel


class SQLAnswerRepository(AnswerRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_answer(self, answer: Answer) -> None:
        """Сохраняет ответ (создает новый или обновляет существующий)."""
        db_answer = AnswerModel(
            question_id=answer.question.id,
            user_id=answer.user.id,
            variant_id=answer.variant.id,
            result_id=answer.result.id
        )
        self.session.add(db_answer)
        await self.session.commit()

    async def get_answer(self, user_id: int, question_id: int) -> Answer:
        """Получить ответ по id пользователя и id вопроса."""
        stmt = select(AnswerModel).where(
            AnswerModel.user_id == user_id,
            AnswerModel.question_id == question_id
        )
        result = await self.session.execute(stmt)
        db_answer = result.scalar_one_or_none()
        if db_answer:
            return Answer(
                question=Question(id=db_answer.question_id, test=Test(id=0, name="", description=""), text="", scoring_rules={}),
                user=User(id=db_answer.user_id),
                variant=Variant(id=db_answer.variant_id, var_text=""),
                result=Result(id=db_answer.result_id, user=User(id=0), test=Test(id=0, name="", description=""), start_time=None, end_time=None, status="")
            )
        raise ValueError("Answer not found")

    async def get_user_answers(self, user_id: int) -> List[Answer]:
        """Получить все ответы пользователя с id."""
        stmt = select(AnswerModel).where(AnswerModel.user_id == user_id)
        result = await self.session.execute(stmt)
        db_answers = result.scalars().all()
        return [
            Answer(
                question=Question(id=a.question_id, test=Test(id=0, name="", description=""), text="", scoring_rules={}),
                user=User(id=a.user_id),
                variant=Variant(id=a.variant_id, var_text=""),
                result=Result(id=a.result_id, user=User(id=0), test=Test(id=0, name="", description=""), start_time=None, end_time=None, status="")
            ) for a in db_answers
        ]

    async def get_question_answers(self, question_id: int) -> List[Answer]:
        """Получить все ответы на вопрос с id."""
        stmt = select(AnswerModel).where(AnswerModel.question_id == question_id)
        result = await self.session.execute(stmt)
        db_answers = result.scalars().all()
        return [
            Answer(
                question=Question(id=a.question_id, test=Test(id=0, name="", description=""), text="", scoring_rules={}),
                user=User(id=a.user_id),
                variant=Variant(id=a.variant_id, var_text=""),
                result=Result(id=a.result_id, user=User(id=0), test=Test(id=0, name="", description=""), start_time=None, end_time=None, status="")
            ) for a in db_answers
        ]

    async def get_answers_by_result(self, result_id: int) -> List[Answer]:
        """Получить ответы из результата с id."""
        stmt = select(AnswerModel).where(AnswerModel.result_id == result_id)
        result = await self.session.execute(stmt)
        db_answers = result.scalars().all()
        return [
            Answer(
                question=Question(id=a.question_id, test=Test(id=0, name="", description=""), text="", scoring_rules={}),
                user=User(id=a.user_id),
                variant=Variant(id=a.variant_id, var_text=""),
                result=Result(id=a.result_id, user=User(id=0), test=Test(id=0, name="", description=""), start_time=None, end_time=None, status="")
            ) for a in db_answers
        ]

    async def get_answers_by_variant(self, variant_id: int) -> List[Answer]:
        """Получить все ответы с вариантом с id."""
        stmt = select(AnswerModel).where(AnswerModel.variant_id == variant_id)
        result = await self.session.execute(stmt)
        db_answers = result.scalars().all()
        return [
            Answer(
                question=Question(id=a.question_id, test=Test(id=0, name="", description=""), text="", scoring_rules={}),
                user=User(id=a.user_id),
                variant=Variant(id=a.variant_id, var_text=""),
                result=Result(id=a.result_id, user=User(id=0), test=Test(id=0, name="", description=""), start_time=None, end_time=None, status="")
            ) for a in db_answers
        ]

    async def delete_answer(self, question_id: int, user_id: int) -> None:
        """Удалить ответ пользователя с id на вопрос с id."""
        stmt = select(AnswerModel).where(
            AnswerModel.question_id == question_id,
            AnswerModel.user_id == user_id
        )
        result = await self.session.execute(stmt)
        db_answer = result.scalar_one_or_none()
        if db_answer:
            await self.session.delete(db_answer)
            await self.session.commit()
        else:
            raise ValueError("Answer not found")

    async def get_all_answers(self) -> List[Answer]:
        """Получить все ответы."""
        stmt = select(AnswerModel)
        result = await self.session.execute(stmt)
        db_answers = result.scalars().all()
        return [
            Answer(
                question=Question(id=a.question_id, test=Test(id=0, name="", description=""), text="", scoring_rules={}),
                user=User(id=a.user_id),
                variant=Variant(id=a.variant_id, var_text=""),
                result=Result(id=a.result_id, user=User(id=0), test=Test(id=0, name="", description=""), start_time=None, end_time=None, status="")
            ) for a in db_answers
        ]

    async def get_user_answers_for_test(self, user_id: int, test_id: int) -> List[Answer]:
        """Получить все ответы пользователя для конкретного теста."""
        # Предполагаем, что нужно связать через ResultModel и TestModel
        stmt = (
            select(AnswerModel)
            .join(ResultModel)
            .where(AnswerModel.user_id == user_id, ResultModel.test_id == test_id)
        )
        result = await self.session.execute(stmt)
        db_answers = result.scalars().all()
        return [
            Answer(
                question=Question(id=a.question_id, test=Test(id=0, name="", description=""), text="", scoring_rules={}),
                user=User(id=a.user_id),
                variant=Variant(id=a.variant_id, var_text=""),
                result=Result(id=a.result_id, user=User(id=0), test=Test(id=0, name="", description=""), start_time=None, end_time=None, status="")
            ) for a in db_answers
        ]