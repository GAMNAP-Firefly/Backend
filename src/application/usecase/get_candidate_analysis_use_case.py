from src.application.dto.CandidateAnalysisDTO import CandidateAnalysisDTO

class GetCandidateAnalysisUseCase:
    def __init__(self, result_repo):
        self.result_repo = result_repo

    def execute(self, link_token: str) -> CandidateAnalysisDTO:
        result = self.result_repo.get_result_by_token(link_token)

        duration = (result.end_time - result.start_time).total_seconds() / 60 if result.end_time else 0

        return CandidateAnalysisDTO(
            test_name=result.test.name,
            start_time=result.start_time.isoformat(),
            end_time=result.end_time.isoformat() if result.end_time else "",
            duration_minutes=round(duration, 2),
            interpretation=result.interpretation or "Анализ не найден"
        ) 