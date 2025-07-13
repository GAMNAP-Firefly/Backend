from typing import Optional

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.service.jwt_service import get_current_user_id
from src.application.usecase.get_question_use_case import GetQuestionUseCase
from src.application.usecase.get_test_questions_use_case import GetTestQuestionsUseCase
from src.infrastructure.db.database import get_async_session
from src.infrastructure.db.repositories.SQLAnswerRepository import SQLAnswerRepository
from src.infrastructure.db.repositories.SQLQuestionRepository import SQLQuestionRepository
from src.infrastructure.db.repositories.SQLVariantRepository import SQLVariantRepository
from src.presentation.schemas.requests.get_question_list_request import GetQuestionListRequest
from src.presentation.schemas.requests.get_question_request import GetQuestionRequest
from src.presentation.schemas.responses.get_question_response import GetQuestionResponse, GetQuestionVariantResponse
from src.presentation.schemas.responses.question_response import QuestionListResponse

router = APIRouter(prefix="/question", tags=["Вопросы"])


@router.get("/list", response_model=Optional[QuestionListResponse], status_code=status.HTTP_200_OK)
async def get_question_list(
        request: GetQuestionListRequest = Depends(),
        session: AsyncSession = Depends(get_async_session)
):
    use_case = GetTestQuestionsUseCase(
        question_repo=SQLQuestionRepository(session)
    )
    try:
        dto = await use_case.execute(test_id=request.test_id)

        if dto is None:
            return None

        questions_id = []
        for question in dto:
            questions_id.append(question.id)
        return QuestionListResponse(questions_id=questions_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=Optional[GetQuestionResponse], status_code=status.HTTP_200_OK)
async def get_question(
        request: GetQuestionRequest = Depends(),
        user_id: int = Depends(get_current_user_id),
        session: AsyncSession = Depends(get_async_session)
):
    use_case = GetQuestionUseCase(
        answer_repo=SQLAnswerRepository(session),
        question_repo=SQLQuestionRepository(session),
        variant_repo=SQLVariantRepository(session)
    )
    try:
        dto = await use_case.execute(question_id=request.question_id, user_id=user_id)
        return GetQuestionResponse(
            id=dto.id,
            text=dto.text,
            variants=[
                GetQuestionVariantResponse(
                    id=v.id,
                    text=v.text,
                    is_selected=v.is_selected
                ) for v in dto.variants
            ]
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
