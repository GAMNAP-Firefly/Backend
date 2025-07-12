from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.usecase.finish_test_use_case import FinishTestUseCase
from src.infrastructure.db.database import get_async_session
from src.infrastructure.db.repositories.SQLAnswerRepository import SQLAnswerRepository
from src.infrastructure.db.repositories.SQLCategoryRepository import SQLCategoryRepository
from src.infrastructure.db.repositories.SQLResultRepository import SQLResultRepository
from src.presentation.schemas.requests.finish_test_request import FinishTestRequest
from src.presentation.schemas.responses.finish_test_response import CategoryScoreResponse, FinishTestResponse, HRShareLinkResponse

router = APIRouter(prefix="/results", tags=["Results"])


@router.post("/finish", response_model=FinishTestResponse, status_code=status.HTTP_200_OK)
async def finish_test(
        request: FinishTestRequest,
        session: AsyncSession = Depends(get_async_session)
):
    use_case = FinishTestUseCase(
        result_repo=SQLResultRepository(session),
        answer_repo=SQLAnswerRepository(session),
        category_repo=SQLCategoryRepository(session),
    )
    try:
        category_scores, hr_share_link = await use_case.execute(result_id=request.result_id)
        
        return FinishTestResponse(
            results=[CategoryScoreResponse(category_name=dto.category_name, score=dto.score) for dto in category_scores],
            share_link=HRShareLinkResponse(share_code=hr_share_link.share_code)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
