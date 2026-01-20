from sqlalchemy.orm import Session
from typing import Optional, List
from app.model.Vehicle import Vehicle
from app.schema.Vehicle import VehicleCreate, VehicleUpdate


class VehicleRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, vehicle_id: int) -> Optional[Vehicle]:
        return self.db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    def get_by_plate_number(self, plate_number: str) -> Optional[Vehicle]:
        return self.db.query(Vehicle).filter(Vehicle.plate_number == plate_number).first()

    def get_all(self, skip: int = 0, limit: int = 100, active_only: bool = False) -> List[Vehicle]:
        query = self.db.query(Vehicle)

        if active_only:
            query = query.filter(Vehicle.is_active == True)

        return query.offset(skip).limit(limit).all()

    def get_by_brand(self, brand: str, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        return (
            self.db.query(Vehicle)
            .filter(Vehicle.brand.ilike(f"%{brand}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_year(self, year: int, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        return (
            self.db.query(Vehicle)
            .filter(Vehicle.year == year)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, vehicle_data: VehicleCreate) -> Vehicle:
        db_vehicle = Vehicle(
            user_id=vehicle_data.user_id,
            plate_number=vehicle_data.plate_number,
            brand=vehicle_data.brand,
            model=vehicle_data.model,
            year=vehicle_data.year
        )
        self.db.add(db_vehicle)
        self.db.commit()
        self.db.refresh(db_vehicle)
        return db_vehicle

    def update(self, vehicle_id: int, vehicle_data: VehicleUpdate) -> Optional[Vehicle]:
        db_vehicle = self.get_by_id(vehicle_id)
        if not db_vehicle:
            return None

        update_data = vehicle_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_vehicle, field, value)

        self.db.commit()
        self.db.refresh(db_vehicle)
        return db_vehicle

    def delete(self, vehicle_id: int) -> bool:
        db_vehicle = self.get_by_id(vehicle_id)
        if not db_vehicle:
            return False

        self.db.delete(db_vehicle)
        self.db.commit()
        return True

    def soft_delete(self, vehicle_id: int) -> Optional[Vehicle]:
        db_vehicle = self.get_by_id(vehicle_id)
        if not db_vehicle:
            return None

        db_vehicle.is_active = False
        self.db.commit()
        self.db.refresh(db_vehicle)
        return db_vehicle

    def exists_by_plate_number(self, plate_number: str) -> bool:
        return self.db.query(Vehicle).filter(Vehicle.plate_number == plate_number).first() is not None

    def count(self, active_only: bool = False) -> int:
        query = self.db.query(Vehicle)

        if active_only:
            query = query.filter(Vehicle.is_active == True)

        return query.count()