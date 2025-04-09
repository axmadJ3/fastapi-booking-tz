from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import Table
from app.schemas.table import TableCreate, TableOut

router = APIRouter(prefix="/tables", tags=["Tables"])

@router.get("/", response_model=list[TableOut])
def get_tables(db: Session = Depends(get_db)):
    """Получает список всех столиков"""
    return db.query(Table).all()

@router.post("/", response_model=TableOut)
def create_table(table: TableCreate, db: Session = Depends(get_db)):
    """Создает новый столик"""
    new_table = Table(**table.dict())
    db.add(new_table)
    db.commit()
    db.refresh(new_table)
    return new_table

@router.delete("/{table_id}")
def delete_table(table_id: int, db: Session = Depends(get_db)):
    """Удаляет столик по ID"""
    table = db.query(Table).get(table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    db.delete(table)
    db.commit()
    return {"detail": "Deleted"}
