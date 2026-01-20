from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.dabatase import get_db
from app.service.PerformanceService import PerformanceService
from app.schema.Performance import PerformanceResponse


router = APIRouter(
    prefix="/api/performances",
    tags=["performances"]
)


def get_performance_service(db: Session = Depends(get_db)) -> PerformanceService:
    return PerformanceService(db)


@router.get("/", response_model=List[PerformanceResponse])
def get_all_performances(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=500, description="Límite de registros"),
    service: PerformanceService = Depends(get_performance_service)
):
    return service.get_all_performances(skip=skip, limit=limit)
