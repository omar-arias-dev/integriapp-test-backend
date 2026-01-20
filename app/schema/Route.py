from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

from app.enum.RouteStatus import RouteStatus

class RouteBase(BaseModel):
    vehicle_id: int = Field(..., description="ID del vehículo asignado")
    origin: str = Field(..., description="Origen de la ruta")
    destination: str = Field(..., description="Destino de la ruta")

class RouteCreate(RouteBase):
    pass

class RouteUpdate(BaseModel):
    status: Optional[RouteStatus] = Field(
        None,
        description="Estado actual de la ruta"
    )


class RouteResponse(RouteBase):
    id: int
    status: RouteStatus
    assigned_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
