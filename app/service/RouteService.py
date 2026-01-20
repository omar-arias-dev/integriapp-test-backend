from typing import List, Dict
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime

from app.repository.RouteRepository import RouteRepository
from app.schema.Route import RouteCreate, RouteUpdate, RouteResponse
from app.schema.RouteComplete import RouteComplete
from app.model.Performance import Performance
from app.enum.RouteStatus import RouteStatus
from app.repository.VehicleRepository import VehicleRepository


class RouteService:

    def __init__(self, db: Session):
        self.repository = RouteRepository(db)
        self.vehicle_repository = VehicleRepository(db)

    def get_route_by_id(self, route_id: int) -> RouteResponse:
        route = self.repository.get_by_id(route_id)
        if not route:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ruta con ID {route_id} no encontrada"
            )
        return RouteResponse.model_validate(route)

    def get_all_routes(
        self,
        skip: int = 0,
        limit: int = 100,
        status: RouteStatus | None = None,
        vehicle_id: int | None = None,
    ) -> List[RouteResponse]:
        routes = self.repository.get_all(
            skip=skip,
            limit=limit,
            status=status,
            vehicle_id=vehicle_id
        )
        return [RouteResponse.model_validate(route) for route in routes]

    def create_route(self, route_data: RouteCreate) -> RouteResponse:
        if not self.vehicle_repository.get_by_id(route_data.vehicle_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Vehículo con ID {route_data.vehicle_id} no existe"
            )

        route = self.repository.create(route_data)
        return RouteResponse.model_validate(route)

    def update_route(self, route_id: int, route_data: RouteUpdate) -> RouteResponse:
        route = self.repository.get_by_id(route_id)

        if not route:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ruta con ID {route_id} no encontrada"
            )

        if (
                route_data.status == RouteStatus.IN_PROGRESS
                and route.started_at is None
        ):
            route.started_at = datetime.now()

        if route_data.status == RouteStatus.COMPLETED:
            route.completed_at = datetime.now()

        updated_route = self.repository.update(route, route_data)

        return RouteResponse.model_validate(updated_route)

    def complete_route(self, route_id: int, payload: RouteComplete):
        route = self.repository.get_by_id(route_id)

        if not route:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ruta no encontrada"
            )

        if route.status == RouteStatus.COMPLETED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La ruta ya fue completada"
            )

        try:
            route.status = RouteStatus.COMPLETED
            route.completed_at = datetime.now()

            performance = Performance(
                route_id=route.id,
                distance_km=payload.distance_km,
                fuel_consumed=payload.fuel_consumed,
                duration=payload.duration_minutes,
                notes=payload.notes
            )

            self.repository.db.add(performance)

            self.repository.db.commit()

            self.repository.db.refresh(route)
            self.repository.db.refresh(performance)

            return {
                "message": "Ruta completada y performance creado",
                "route_id": route.id
            }

        except Exception:
            self.repository.db.rollback()
            raise

    def delete_route(self, route_id: int) -> Dict[str, str]:
        if not self.repository.delete(route_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ruta con ID {route_id} no encontrada"
            )
        return {"message": f"Ruta {route_id} eliminada correctamente"}
