from fastapi import APIRouter, HTTPException
from models.schemas import UserCreate

router = APIRouter()

users_db: list[dict] = []

@router.post("/register", status_code=201)
def register(user: UserCreate):
    exists = any(u["email"] == user.email for u in users_db)
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = {"id": len(users_db) + 1, **user.model_dump()}
    users_db.append(new_user)
    return {"message": "User registered", "id": new_user["id"]}

@router.get("/")
def list_users():
    return [{"id": u["id"], "name": u["name"], "email": u["email"]} for u in users_db]