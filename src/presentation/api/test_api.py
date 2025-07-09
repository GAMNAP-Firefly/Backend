from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.service.jwt_service import get_current_user_id
from src.application.usecase.start_test_use_case import StartTestUseCase
from src.infrastructure.db.database import get_async_session
from src.infrastructure.db.repositories.SQLAnswerRepository import SQLAnswerRepository
from src.infrastructure.db.repositories.SQLQuestionRepository import SQLQuestionRepository
from src.infrastructure.db.repositories.SQLResultRepository import SQLResultRepository
from src.infrastructure.db.repositories.SQLTestRepository import SQLTestRepository
from src.infrastructure.db.repositories.SQLUserRepository import SQLUserRepository
from src.infrastructure.db.repositories.SQLVariantRepository import SQLVariantRepository
from src.presentation.schemas.requests.start_test_request import StartTestRequest
from src.presentation.schemas.responses.question_response import QuestionResponse
from src.presentation.schemas.responses.test_response import StartTestResponse

router = APIRouter(prefix="/tests", tags=["Tests"])


@router.post("/start", response_model=StartTestResponse, status_code=status.HTTP_201_CREATED)
async def start_test(
        request: StartTestRequest,
        user_id: int = Depends(get_current_user_id),
        session: AsyncSession = Depends(get_async_session)
):
    use_case = StartTestUseCase(
        result_repo=SQLResultRepository(session),
        question_repo=SQLQuestionRepository(session),
        variant_repo=SQLVariantRepository(session),
        user_repo=SQLUserRepository(session),
        test_repo=SQLTestRepository(session),
        answer_repo=SQLAnswerRepository(session),
    )
    try:
        dto = await use_case.execute(user_id=user_id, test_id=request.test_id)
        question = dto.question
        return StartTestResponse(
            result_id=dto.result_id,
            question=QuestionResponse(
                id=question.id,
                text=question.text,
                index=question.index,
                total=question.total,
                progress_percent=question.progress_percent,
                variants=[
                    {"id": v.id, "text": v.text, "is_selected": v.is_selected} for v in question.variants
                ]
            )
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
