from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.dabatase import get_db
from app.service.VehicleService import VehicleService
from app.schema.Vehicle import VehicleCreate, VehicleUpdate, VehicleResponse


router = APIRouter(
    prefix="/api/vehicles",
    tags=["vehicles"]
)


def get_vehicle_service(db: Session = Depends(get_db)) -> VehicleService:
    return VehicleService(db)


@router.get("/", response_model=List[VehicleResponse])
def get_all_vehicles(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=500, description="Límite de registros"),
    active_only: bool = Query(False, description="Filtrar solo vehículos activos"),
    service: VehicleService = Depends(get_vehicle_service)
):
    return service.get_all_vehicles(skip=skip, limit=limit, active_only=active_only)


@router.get("/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle(
    vehicle_id: int,
    service: VehicleService = Depends(get_vehicle_service)
):
    return service.get_vehicle_by_id(vehicle_id)


@router.post("/", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
def create_vehicle(
    vehicle_data: VehicleCreate,
    service: VehicleService = Depends(get_vehicle_service)
):
    return service.create_vehicle(vehicle_data)


@router.put("/{vehicle_id}", response_model=VehicleResponse)
def update_vehicle(
    vehicle_id: int,
    vehicle_data: VehicleUpdate,
    service: VehicleService = Depends(get_vehicle_service)
):
    return service.update_vehicle(vehicle_id, vehicle_data)


@router.patch("/{vehicle_id}/deactivate", response_model=VehicleResponse)
def deactivate_vehicle(
    vehicle_id: int,
    service: VehicleService = Depends(get_vehicle_service)
):
    update_data = VehicleUpdate(is_active=False)
    return service.update_vehicle(vehicle_id, update_data)


@router.patch("/{vehicle_id}/activate", response_model=VehicleResponse)
def activate_vehicle(
    vehicle_id: int,
    service: VehicleService = Depends(get_vehicle_service)
):
    update_data = VehicleUpdate(is_active=True)
    return service.update_vehicle(vehicle_id, update_data)


@router.delete("/{vehicle_id}", status_code=status.HTTP_200_OK)
def delete_vehicle(
    vehicle_id: int,
    soft: bool = Query(True, description="Soft delete (True) o Hard delete (False)"),
    service: VehicleService = Depends(get_vehicle_service)
):
    return service.delete_vehicle(vehicle_id, soft=soft)