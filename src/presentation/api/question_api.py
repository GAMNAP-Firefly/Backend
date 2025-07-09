from typing import Optional

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.service.jwt_service import get_current_user_id
from src.application.usecase.get_next_question_use_case import GetNextQuestionUseCase
from src.infrastructure.db.database import get_async_session
from src.infrastructure.db.repositories.SQLAnswerRepository import SQLAnswerRepository
from src.infrastructure.db.repositories.SQLQuestionRepository import SQLQuestionRepository
from src.infrastructure.db.repositories.SQLVariantRepository import SQLVariantRepository
from src.presentation.schemas.requests.get_next_question_request import GetNextQuestionRequest
from src.presentation.schemas.responses.question_response import QuestionResponse

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.post("/next", response_model=Optional[QuestionResponse], status_code=status.HTTP_200_OK)
async def get_next_question(
        request: GetNextQuestionRequest,
        user_id: int = Depends(get_current_user_id),
        session: AsyncSession = Depends(get_async_session)
):
    use_case = GetNextQuestionUseCase(
        answer_repo=SQLAnswerRepository(session),
        question_repo=SQLQuestionRepository(session),
        variant_repo=SQLVariantRepository(session),
    )
    try:
        dto = await use_case.execute(user_id=user_id, test_id=request.test_id)
        if dto is None:
            return None
        return QuestionResponse(
            id=dto.id,
            text=dto.text,
            index=dto.index,
            total=dto.total,
            progress_percent=dto.progress_percent,
            variants=[
                {"id": v.id, "text": v.text, "is_selected": v.is_selected} for v in dto.variants
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
