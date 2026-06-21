from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import db_models
from models.schemas import UserCreate

router = APIRouter()

@router.post("/register", status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(db_models.User).filter(db_models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = db_models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered", "id": new_user.id}

@router.get("/")
def list_users(db: Session = Depends(get_db)):
    users = db.query(db_models.User).all()
    return [{"id": u.id, "name": u.name, "email": u.email, "role": u.role} for u in users]