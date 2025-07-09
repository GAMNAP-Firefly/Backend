from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.repository.QuestionRepository import QuestionRepository
from src.domain.entity.Question import Question
from src.domain.entity.Test import Test
from src.infrastructure.db.models.question_model import QuestionModel
from sqlalchemy import select
from typing import List

class SQLQuestionRepository(QuestionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_question(self, question: Question) -> None:
        """Добавить вопрос."""
        db_question = QuestionModel(
            id=question.id,
            test_id=question.test.id,
            text=question.text,
            scoring_rules=question.scoring_rules
        )
        self.session.add(db_question)
        await self.session.commit()

    async def get_question(self, question_id) -> Question:
        """Получить вопрос с id."""
        db_question = await self.session.get(QuestionModel, question_id)
        if db_question:
            return Question(
                id=db_question.id,
                test=Test(id=db_question.test_id, name="", description=""),
                text=db_question.text,
                scoring_rules=db_question.scoring_rules
            )
        raise ValueError("Question not found")

    async def get_test_questions(self, test_id) -> List[Question]:
        """Получить вопросы в тесте с id."""
        stmt = select(QuestionModel).where(QuestionModel.test_id == test_id)
        result = await self.session.execute(stmt)
        db_questions = result.scalars().all()
        return [
            Question(
                id=q.id,
                test=Test(id=q.test_id, name="", description=""),
                text=q.text,
                scoring_rules=q.scoring_rules
            ) for q in db_questions
        ]

    async def delete_test_question(self, question_id) -> None:
        """Удалить вопрос с id."""
        db_question = await self.session.get(QuestionModel, question_id)
        if db_question:
            await self.session.delete(db_question)
            await self.session.commit()
        else:
            raise ValueError("Question not found")

    async def edit_question(self, question_id: int, question: Question) -> None:
        """Изменить вопрос с id."""
        db_question = await self.session.get(QuestionModel, question_id)
        if db_question:
            db_question.test_id = question.test.id
            db_question.text = question.text
            db_question.scoring_rules = question.scoring_rules
            await self.session.commit()
        else:
            raise ValueError("Question not found")

    async def get_all_questions(self) -> List[Question]:
        """Получить все вопросы."""
        stmt = select(QuestionModel)
        result = await self.session.execute(stmt)
        db_questions = result.scalars().all()
        return [
            Question(
                id=q.id,
                test=Test(id=q.test_id, name="", description=""),
                text=q.text,
                scoring_rules=q.scoring_rules
            ) for q in db_questions
        ]