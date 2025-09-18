from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.database import get_async_session
from src.infrastructure.db.repositories.SQLUserRepository import SQLUserRepository
from src.infrastructure.db.repositories.SQLTestRepository import SQLTestRepository
from src.infrastructure.db.repositories.SQLQuestionRepository import SQLQuestionRepository
from src.infrastructure.db.repositories.SQLAnswerRepository import SQLAnswerRepository
from src.infrastructure.db.repositories.SQLResultRepository import SQLResultRepository
from src.infrastructure.db.repositories.SQLCategoryRepository import SQLCategoryRepository
from src.infrastructure.db.repositories.SQLVariantRepository import SQLVariantRepository
from src.domain.repository.UserRepository import UserRepository
from src.domain.repository.TestRepository import TestRepository
from src.domain.repository.QuestionRepository import QuestionRepository
from src.domain.repository.AnswerRepository import AnswerRepository
from src.domain.repository.ResultRepository import ResultRepository
from src.domain.repository.CategoryRepository import CategoryRepository
from src.domain.repository.VariantRepository import VariantRepository


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