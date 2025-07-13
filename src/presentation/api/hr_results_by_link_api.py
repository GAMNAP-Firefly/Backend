from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.usecase.get_hr_results_by_link_use_case import GetHRResultsByLinkUseCase
from src.infrastructure.db.database import get_async_session
from src.infrastructure.db.repositories.SQLAnswerRepository import SQLAnswerRepository
from src.infrastructure.db.repositories.SQLCategoryRepository import SQLCategoryRepository
from src.infrastructure.db.repositories.SQLResultRepository import SQLResultRepository
from src.infrastructure.db.repositories.SQLTestRepository import SQLTestRepository
from src.presentation.schemas.requests.hr_results_by_link_request import HRResultsByLinkRequest
from src.presentation.schemas.responses.hr_results_by_link_response import HRResultsByLinkResponse

router = APIRouter(prefix="/hr/share", tags=["HR Results by Link"])


@router.post("/results", response_model=HRResultsByLinkResponse, status_code=status.HTTP_200_OK)
async def get_hr_results_by_link(
        request: HRResultsByLinkRequest,
        session: AsyncSession = Depends(get_async_session)
):
    """
    Получает результаты теста по ссылке для HR.
    Позволяет HR просматривать результаты кандидата по уникальному коду.
    """
    use_case = GetHRResultsByLinkUseCase(
        result_repo=SQLResultRepository(session),
        answer_repo=SQLAnswerRepository(session),
        category_repo=SQLCategoryRepository(session),
        test_repo=SQLTestRepository(session),
    )
    try:
        candidate_analysis, category_scores = await use_case.execute(share_code=request.share_code)
        
        return HRResultsByLinkResponse(
            candidate_analysis={
                "test_name": candidate_analysis.test_name,
                "start_time": candidate_analysis.start_time,
                "end_time": candidate_analysis.end_time,
                "duration_minutes": candidate_analysis.duration_minutes,
                "interpretation": candidate_analysis.interpretation
            },
            category_scores=[
                {
                    "category_name": dto.category_name,
                    "score": dto.score
                } for dto in category_scores
            ]
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 