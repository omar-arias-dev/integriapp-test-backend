from sqlalchemy import Column, Integer, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, UTC

from app.core.dabatase import Base


class Performance(Base):
    __tablename__ = "performances"

    route_id = Column(
        Integer,
        ForeignKey("routes.id", ondelete="CASCADE"),
        primary_key=True
    )
    distance_km = Column(Float, nullable=False)
    fuel_consumed = Column(Float, nullable=False)
    duration = Column(Integer, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False
    )

    route = relationship("Route", back_populates="performance", uselist=False)
