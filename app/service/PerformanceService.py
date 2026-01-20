from typing import List

from app.repository.PerformanceRepository import PerformanceRepository
from app.schema.Performance import PerformanceResponse


class PerformanceService:

    def __init__(self, db):
        self.repository = PerformanceRepository(db)

    def get_all_performances(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> List[PerformanceResponse]:
        performances = self.repository.get_all(skip=skip, limit=limit)
        return [
            PerformanceResponse.model_validate(performance)
            for performance in performances
        ]
