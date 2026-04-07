from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.database import get_db
from app.models.record_model import Record
from app.middleware.role_check import role_required

router = APIRouter(
    dependencies=[Depends(role_required(["admin", "analyst"]))]
)

@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):

    total_income = db.query(func.sum(Record.amount))\
        .filter(Record.type == "income")\
        .scalar() or 0

    total_expense = db.query(func.sum(Record.amount))\
        .filter(Record.type == "expense")\
        .scalar() or 0

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": total_income - total_expense
    }

@router.get("/category")
def category_summary(db: Session = Depends(get_db)):

    result = db.query(
        Record.category,
        func.sum(Record.amount)
    ).group_by(Record.category).all()

    return [
        {"category": r[0], "total": r[1]}
        for r in result
    ]

@router.get("/trends")
def monthly_trends(db: Session = Depends(get_db)):

    result = db.query(
        func.substr(Record.date, 1, 7),  # YYYY-MM
        func.sum(Record.amount)
    ).group_by(func.substr(Record.date, 1, 7)).all()

    return [
        {"month": r[0], "total": r[1]}
        for r in result
    ]

