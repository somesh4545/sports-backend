from fastapi import APIRouter
from models.index import Users
from schemas.index import User
from sqlalchemy.orm import Session 
from fastapi import Depends
from config.db import get_db

userRouter = APIRouter()

@userRouter.get('/')
async def fetch_all_users(db: Session = Depends(get_db)):
    return db.query(Users).all()

# @userRouter.get('/{id}')
# async def fetch_by_id(id: int):
#     return conn.execute(users.select().where(users.c.id == id)).fetchall()

@userRouter.post('/')
async def create_user(user: User, db: Session = Depends(get_db)):
    user_item = Users(name=user.name, email=user.email)
    db.add(user_item)
    db.commit()
    db.refresh(user_item)
    return user_item    