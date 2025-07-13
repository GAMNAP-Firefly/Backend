from typing import Optional

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.usecase.get_test_questions_use_case import GetTestQuestionsUseCase
from src.infrastructure.db.database import get_async_session
from src.infrastructure.db.repositories.SQLQuestionRepository import SQLQuestionRepository
from src.presentation.schemas.requests.get_question_list_request import GetQuestionListRequest
from src.presentation.schemas.responses.question_response import QuestionListResponse

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.post("/list", response_model=Optional[QuestionListResponse], status_code=status.HTTP_200_OK)
async def get_question_list(
        request: GetQuestionListRequest,
        session: AsyncSession = Depends(get_async_session)
):
    use_case = GetTestQuestionsUseCase(
        question_repo=SQLQuestionRepository(session)
    )
    try:
        dto = await use_case.execute(test_id=request.test_id)

        if dto is None:
            return None

        questions_id=[]
        for question in dto:
            questions_id.append(question.id)
        return QuestionListResponse(questions_id=questions_id)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
