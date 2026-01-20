from sqlalchemy.orm import Session
from typing import List, Optional

from app.model.Performance import Performance


class PerformanceRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_route_id(self, route_id: int) -> Optional[Performance]:
        return (
            self.db
            .query(Performance)
            .filter(Performance.route_id == route_id)
            .first()
        )

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Performance]:
        return (
            self.db
            .query(Performance)
            .order_by(Performance.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, performance: Performance) -> Performance:
        self.db.add(performance)
        self.db.commit()
        self.db.refresh(performance)
        return performance

    def delete(self, route_id: int) -> bool:
        performance = self.get_by_route_id(route_id)
        if not performance:
            return False

        self.db.delete(performance)
        self.db.commit()
        return True
