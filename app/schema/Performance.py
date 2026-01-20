from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime


class PerformanceBase(BaseModel):
    route_id: int = Field(..., description="ID de la ruta asociada")
    distance_km: float = Field(..., gt=0, description="Distancia recorrida en kilómetros")
    fuel_consumed: float = Field(..., ge=0, description="Combustible consumido")
    duration_minutes: int = Field(..., gt=0, description="Duración del viaje en minutos")
    notes: Optional[str] = Field(None, description="Notas adicionales del performance")


class PerformanceCreate(PerformanceBase):
    pass


class PerformanceResponse(PerformanceBase):
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
