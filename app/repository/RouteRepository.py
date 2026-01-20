from sqlalchemy.orm import Session
from typing import Optional, List

from app.model.Route import Route
from app.schema.Route import RouteCreate, RouteUpdate
from app.enum.RouteStatus import RouteStatus


class RouteRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, route_id: int) -> Optional[Route]:
        return self.db.query(Route).filter(Route.id == route_id).first()

    def get_all(
            self,
            skip: int = 0,
            limit: int = 100,
            status: Optional[RouteStatus] = None,
            vehicle_id: Optional[int] = None,
    ) -> List[Route]:
        query = self.db.query(Route)

        if status:
            query = query.filter(Route.status == status)

        if vehicle_id is not None:
            query = query.filter(Route.vehicle_id == vehicle_id)

        return query.offset(skip).limit(limit).all()

    def create(self, route_data: RouteCreate) -> Route:
        db_route = Route(
            vehicle_id=route_data.vehicle_id,
            origin=route_data.origin,
            destination=route_data.destination,
        )

        self.db.add(db_route)
        self.db.commit()
        self.db.refresh(db_route)
        return db_route

    def update(self, route: Route, route_data: RouteUpdate) -> Route:
        for field, value in route_data.model_dump(exclude_unset=True).items():
            setattr(route, field, value)

        self.db.commit()
        self.db.refresh(route)
        return route

    def delete(self, route_id: int) -> bool:
        db_route = self.get_by_id(route_id)
        if not db_route:
            return False

        self.db.delete(db_route)
        self.db.commit()
        return True

