from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional


class VehicleBase(BaseModel):
    user_id: Optional[int] = Field(None, description="ID del usuario propietario")
    plate_number: str = Field(..., description="Número de placa del vehículo")
    brand: str = Field(..., description="Marca del vehículo")
    model: str = Field(..., description="Modelo del vehículo")
    year: Optional[int] = Field(None, ge=1900, le=2100, description="Año del vehículo")


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(BaseModel):
    user_id: Optional[int] = None
    plate_number: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = Field(None, ge=1900, le=2100)
    is_active: Optional[bool] = None


class VehicleResponse(VehicleBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)