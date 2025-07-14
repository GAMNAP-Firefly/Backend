from typing import Optional

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.dto.GetUserTestStatisticsDTO import GetUserTestStatisticsDTO
from src.application.service.jwt_service import get_current_user_id
from src.application.usecase.get_user_test_statistics_use_case import GetUserTestStatisticsUseCase
from src.application.usecase.submit_answer_use_case import SubmitAnswerUseCase
from src.infrastructure.db.database import get_async_session
from src.infrastructure.db.repositories.SQLAnswerRepository import SQLAnswerRepository
from src.infrastructure.db.repositories.SQLQuestionRepository import SQLQuestionRepository
from src.infrastructure.db.repositories.SQLResultRepository import SQLResultRepository
from src.infrastructure.db.repositories.SQLTestRepository import SQLTestRepository
from src.infrastructure.db.repositories.SQLUserRepository import SQLUserRepository
from src.infrastructure.db.repositories.SQLVariantRepository import SQLVariantRepository
from src.presentation.schemas.requests.answer_request import SubmitAnswerRequest
from src.presentation.schemas.requests.get_user_test_statistics_request import GetUserTestStatisticsRequest
from src.presentation.schemas.responses.get_user_test_statistics_response import GetUserTestStatisticsResponse

router = APIRouter(prefix="/answer", tags=["Ответы"])


@router.post("/submit", status_code=status.HTTP_204_NO_CONTENT)
async def submit_answer(
        request: SubmitAnswerRequest,
        user_id: int = Depends(get_current_user_id),
        session: AsyncSession = Depends(get_async_session)
):
    use_case = SubmitAnswerUseCase(
        answer_repo=SQLAnswerRepository(session),
        question_repo=SQLQuestionRepository(session),
        variant_repo=SQLVariantRepository(session),
        result_repo=SQLResultRepository(session),
        user_repo=SQLUserRepository(session),
    )
    try:
        await use_case.execute(
            user_id=user_id,
            question_id=request.question_id,
            variant_id=request.variant_id,
            result_id=request.result_id
        )
        return  # 204 No Content
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/statistics", response_model=Optional[GetUserTestStatisticsResponse], status_code=status.HTTP_200_OK)
async def get_user_test_statistics(
        request: GetUserTestStatisticsRequest = Depends(),
        session: AsyncSession = Depends(get_async_session)
):
    use_case = GetUserTestStatisticsUseCase(
        result_repo=SQLResultRepository(session),
        question_repo=SQLQuestionRepository(session),
        answer_repo=SQLAnswerRepository(session)
    )
    try:
        result_dto: GetUserTestStatisticsDTO = await use_case.execute(
            result_id=request.result_id
        )
        return GetUserTestStatisticsResponse(total_questions=result_dto.total_questions,
                                             progress_percent=result_dto.progress_percent)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
