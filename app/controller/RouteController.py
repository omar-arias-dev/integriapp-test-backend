from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.dabatase import get_db
from app.service.RouteService import RouteService
from app.schema.Route import RouteCreate, RouteUpdate, RouteResponse
from app.schema.RouteComplete import RouteComplete
from app.enum.RouteStatus import RouteStatus

router = APIRouter(
    prefix="/api/routes",
    tags=["routes"]
)


def get_route_service(db: Session = Depends(get_db)) -> RouteService:
    return RouteService(db)


@router.get("/", response_model=List[RouteResponse])
def get_all_routes(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=500, description="Límite de registros"),
    status: Optional[RouteStatus] = Query(None, description="Estado de la ruta"),
    vehicle_id: Optional[int] = Query(None, description="ID del vehículo"),
    service: RouteService = Depends(get_route_service)
):
    return service.get_all_routes(
        skip=skip,
        limit=limit,
        status=status,
        vehicle_id=vehicle_id
    )

@router.get("/{route_id}", response_model=RouteResponse)
def get_route(
    route_id: int,
    service: RouteService = Depends(get_route_service)
):
    return service.get_route_by_id(route_id)


@router.post("/", response_model=RouteResponse, status_code=status.HTTP_201_CREATED)
def create_route(
    route_data: RouteCreate,
    service: RouteService = Depends(get_route_service)
):
    return service.create_route(route_data)


@router.put("/{route_id}", response_model=RouteResponse)
def update_route(
    route_id: int,
    route_data: RouteUpdate,
    service: RouteService = Depends(get_route_service)
):
    return service.update_route(route_id, route_data)


@router.delete("/{route_id}", status_code=status.HTTP_200_OK)
def delete_route(
    route_id: int,
    service: RouteService = Depends(get_route_service)
):
    return service.delete_route(route_id)

@router.patch("/{route_id}/complete", status_code=status.HTTP_200_OK)
def complete_route(
    route_id: int,
    payload: RouteComplete,
    service: RouteService = Depends(get_route_service)
):
    return service.complete_route(route_id, payload)

