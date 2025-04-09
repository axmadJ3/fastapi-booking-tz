from datetime import datetime
from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Table(Base):
    __tablename__ = "restaurant_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    seats: Mapped[int] = mapped_column(nullable=True)
    location: Mapped[str] = mapped_column(String(100))
    
    reservations: Mapped[List["Reservation"]] = relationship(back_populates="table")
    
    def __repr__(self) -> str:
        return (
            f"Table(id={self.id!r}, name={self.name!r}, "
            f"seats={self.seats!r}, location={self.location!r})"
        )


class Reservation(Base):
    __tablename__ = "reservation_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_name: Mapped[str] = mapped_column(String(50))
    table_id: Mapped[int] = mapped_column(ForeignKey("restaurant_table.id"))
    reservation_time: Mapped[datetime]
    duration_minutes: Mapped[int]
    
    table: Mapped["Table"] = relationship(back_populates="reservations")
    
    def __repr__(self) -> str:
        return (
            f"Reservation(id={self.id!r}, customer_name={self.customer_name!r}, "
            f"table_id={self.table_id!r}, reservation_time={self.reservation_time!r}, "
            f"duration_minutes={self.duration_minutes!r})"
        )
