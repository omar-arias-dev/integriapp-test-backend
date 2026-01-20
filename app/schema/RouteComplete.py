from pydantic import BaseModel, Field
from typing import Optional


class RouteComplete(BaseModel):
    distance_km: float = Field(..., gt=0, description="Distancia recorrida en km")
    fuel_consumed: float = Field(..., ge=0, description="Combustible consumido en litros")
    duration_minutes: int = Field(..., gt=0, description="Duración total en minutos")
    notes: Optional[str] = Field(None, description="Notas del desempeño")
