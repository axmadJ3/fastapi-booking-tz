from sqlalchemy.orm import Session
from app.models.models import Reservation
from datetime import timedelta

def is_conflict(db: Session, table_id: int, start_time, duration_minutes: int) -> bool:
    """"Проверяет, есть ли конфликт с существующими бронированиями"""
    end_time = start_time + timedelta(minutes=duration_minutes)
    conflicting = db.query(Reservation).filter(
        Reservation.table_id == table_id,
        Reservation.reservation_time < end_time,
        (Reservation.reservation_time + timedelta(minutes=Reservation.duration_minutes)) > start_time
    ).first()
    return conflicting is not None
