from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from app.schemas.record_schema import RecordCreate
from app.models.record_model import Record
from app.db.database import get_db
from sqlalchemy import func
from app.middleware.role_check import role_required
from fastapi import HTTPException


router = APIRouter()


@router.post("/")
def create_record(record: RecordCreate, db: Session = Depends(get_db),
                  role: str = Depends(role_required(["admin"]))
                  ):
    new_record = Record(**record.dict())

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return new_record


@router.get("/")
def get_records(
    type: str = Query(None),
    category: str = Query(None),
    limit: int = Query(10),
    offset: int = Query(0),
    db: Session = Depends(get_db),
    role: str = Depends(role_required(["admin", "analyst", "viewer"]))
):
    query = db.query(Record)


    if type:
        query = query.filter(Record.type == type)

    if category:
        query = query.filter(func.lower(Record.category) == category.lower())

    return query.offset(offset).limit(limit).all()

@router.put("/{id}")
def update_record(
    id: int,
    data: RecordCreate,
    db: Session = Depends(get_db),
    role: str = Depends(role_required(["admin"]))  # ✅
):
    record = db.query(Record).filter(Record.id == id).first()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    for key, value in data.dict().items():
        setattr(record, key, value)

    db.commit()
    return record

@router.delete("/{id}")
def delete_record(
    id: int,
    db: Session = Depends(get_db),
    role: str = Depends(role_required(["admin"]))  # ✅
):
    record = db.query(Record).filter(Record.id == id).first()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    db.delete(record)
    db.commit()

    return {"message": "Deleted"}