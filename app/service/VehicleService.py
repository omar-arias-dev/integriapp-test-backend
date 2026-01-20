from sqlalchemy.orm import Session
from typing import List, Dict
from fastapi import HTTPException, status

from app.repository.VehicleRepository import VehicleRepository
from app.schema.Vehicle import VehicleCreate, VehicleUpdate, VehicleResponse


class VehicleService:

    def __init__(self, db: Session):
        self.repository = VehicleRepository(db)

    def get_vehicle_by_id(self, vehicle_id: int) -> VehicleResponse:
        vehicle = self.repository.get_by_id(vehicle_id)
        if not vehicle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vehículo con ID {vehicle_id} no encontrado"
            )
        return VehicleResponse.model_validate(vehicle)

    def get_all_vehicles(
            self,
            skip: int = 0,
            limit: int = 100,
            active_only: bool = False
    ) -> List[VehicleResponse]:
        vehicles = self.repository.get_all(skip=skip, limit=limit, active_only=active_only)
        return [VehicleResponse.model_validate(vehicle) for vehicle in vehicles]

    def create_vehicle(self, vehicle_data: VehicleCreate) -> VehicleResponse:
        if self.repository.exists_by_plate_number(vehicle_data.plate_number):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un vehículo con la placa {vehicle_data.plate_number}"
            )

        if not self._validate_plate_format(vehicle_data.plate_number):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de placa inválido"
            )

        vehicle = self.repository.create(vehicle_data)
        return VehicleResponse.model_validate(vehicle)

    def update_vehicle(self, vehicle_id: int, vehicle_data: VehicleUpdate) -> VehicleResponse:
        if not self.repository.get_by_id(vehicle_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vehículo con ID {vehicle_id} no encontrado"
            )

        if vehicle_data.plate_number:
            existing_vehicle = self.repository.get_by_plate_number(vehicle_data.plate_number)
            if existing_vehicle and existing_vehicle.id != vehicle_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe un vehículo con la placa {vehicle_data.plate_number}"
                )

            if not self._validate_plate_format(vehicle_data.plate_number):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Formato de placa inválido"
                )

        vehicle = self.repository.update(vehicle_id, vehicle_data)
        return VehicleResponse.model_validate(vehicle)

    def delete_vehicle(self, vehicle_id: int, soft: bool = True) -> Dict[str, str]:
        if soft:
            vehicle = self.repository.soft_delete(vehicle_id)
            if not vehicle:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Vehículo con ID {vehicle_id} no encontrado"
                )
            return {"message": f"Vehículo {vehicle_id} marcado como inactivo"}
        else:
            if not self.repository.delete(vehicle_id):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Vehículo con ID {vehicle_id} no encontrado"
                )
            return {"message": f"Vehículo {vehicle_id} eliminado permanentemente"}

    def _validate_plate_format(self, plate_number: str) -> bool:
        import re
        pattern = r'^[A-Z0-9-]{3,10}$'
        return bool(re.match(pattern, plate_number.upper()))