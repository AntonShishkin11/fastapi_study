from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.models import Users
from database.session import get_async_session
from services.pass_service import PasswordService as p
from services.token_service import create_token

router = APIRouter(prefix="/auth", tags=["Auth"])

class UserIn(BaseModel):
    username: str
    password: str

@router.post("/register")
async def register(user: UserIn, db: AsyncSession = Depends(get_async_session)):
    res = await db.execute(select(Users).where(Users.username == user.username))
    if res.scalar():
        raise HTTPException(status_code=400, detail="User already exists")

    user_db = Users(username=user.username, password_hash=p.hash_password(user.password))
    db.add(user_db)
    await db.commit()
    return {"message": "User created"}

@router.post("/login")
async def login(user: UserIn, db: AsyncSession = Depends(get_async_session)):
    res = await db.execute(select(Users).where(Users.username == user.username))
    user_db = res.scalar()

    if not user_db or not p.verify_password(user.password, user_db.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"sub": user.username})
    return {"access_token": token}

@router.post("/logout")
async def logout():
    return {"message": "Logout client-side only — delete token manually"}
