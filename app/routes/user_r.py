from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate
from app.models.user_model import User
from app.db.database import get_db
from fastapi import HTTPException
from app.middleware.role_check import role_required

router = APIRouter()

@router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        name=user.name,
        email=user.email,
        role=user.role,
        status="active"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.put("/{id}")
def update_user(
    id: int,
    data: UserCreate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = data.name
    user.email = data.email
    user.role = data.role

    db.commit()
    db.refresh(user)

    return user


@router.patch("/{id}/status")
def change_status(
    id: int,
    status: str,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if status not in ["active", "inactive"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    user.status = status
    db.commit()

    return {"message": "Status updated"}

@router.delete("/{id}")
def delete_user(
    id: int,
    db: Session = Depends(get_db),
    role: str = Depends(role_required(["admin"]))  # only admin
):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}