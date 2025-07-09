from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db.database import get_async_session
from infrastructure.db.repositories.SQLUserRepository import SQLUserRepository
from infrastructure.db.repositories.SQLTestRepository import SQLTestRepository
from infrastructure.db.repositories.SQLQuestionRepository import SQLQuestionRepository
from infrastructure.db.repositories.SQLAnswerRepository import SQLAnswerRepository
from infrastructure.db.repositories.SQLResultRepository import SQLResultRepository
from infrastructure.db.repositories.SQLCategoryRepository import SQLCategoryRepository
from infrastructure.db.repositories.SQLVariantRepository import SQLVariantRepository
from domain.repository.UserRepository import UserRepository
from domain.repository.TestRepository import TestRepository
from domain.repository.QuestionRepository import QuestionRepository
from domain.repository.AnswerRepository import AnswerRepository
from domain.repository.ResultRepository import ResultRepository
from domain.repository.CategoryRepository import CategoryRepository
from domain.repository.VariantRepository import VariantRepository


# Dependency для получения репозиториев
def get_user_repository(session: Annotated[AsyncSession, Depends(get_async_session)]) -> UserRepository:
    return SQLUserRepository(session)

def get_test_repository(session: Annotated[AsyncSession, Depends(get_async_session)]) -> TestRepository:
    return SQLTestRepository(session)

def get_question_repository(session: Annotated[AsyncSession, Depends(get_async_session)]) -> QuestionRepository:
    return SQLQuestionRepository(session)

def get_answer_repository(session: Annotated[AsyncSession, Depends(get_async_session)]) -> AnswerRepository:
    return SQLAnswerRepository(session)

def get_result_repository(session: Annotated[AsyncSession, Depends(get_async_session)]) -> ResultRepository:
    return SQLResultRepository(session)

def get_category_repository(session: Annotated[AsyncSession, Depends(get_async_session)]) -> CategoryRepository:
    return SQLCategoryRepository(session)

def get_variant_repository(session: Annotated[AsyncSession, Depends(get_async_session)]) -> VariantRepository:
    return SQLVariantRepository(session) 