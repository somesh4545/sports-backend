from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from models.index import Students
from schemas.index import Student
from sqlalchemy.orm import Session 
from fastapi import Depends
from config.db import get_db

studentsRouter = APIRouter()

@studentsRouter.get('/')
async def fetch_all_student(db: Session = Depends(get_db)):
    return db.query(Students).all()

@studentsRouter.post('/')
async def create_student(student: Student, db: Session = Depends(get_db)):
    stud_item = Students(name=student.name, email=student.email)
    db.add(stud_item)
    db.commit()
    db.refresh(stud_item)
    return stud_item

@studentsRouter.get('/{id}')
async def get_by_id(id, db: Session = Depends(get_db)):
    student = db.query(Students).filter(Students.id == id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


