from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import Reservation
from app.schemas.reservation import ReservationCreate, ReservationOut
from app.services.reservation_service import is_conflict

router = APIRouter(prefix="/reservations", tags=["Reservations"])

@router.get("/", response_model=list[ReservationOut])
def get_reservations(db: Session = Depends(get_db)):
    """Получает список всех бронирований"""
    return db.query(Reservation).all()

@router.post("/", response_model=ReservationOut)
def create_reservation(res: ReservationCreate, db: Session = Depends(get_db)):
    """Создает новое бронирование"""
    if is_conflict(db, res.table_id, res.reservation_time, res.duration_minutes):
        raise HTTPException(status_code=409, detail="Столик уже забронирован на это время")
    new_res = Reservation(**res.dict())
    db.add(new_res)
    db.commit()
    db.refresh(new_res)
    return new_res

@router.delete("/{reservation_id}")
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    """Удаляет бронирование по ID"""
    reservation = db.query(Reservation).get(reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Бронирование не найдено")
    db.delete(reservation)
    db.commit()
    return {"detail": "Deleted"}
