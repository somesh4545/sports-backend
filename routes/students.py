from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from models.index import Students, Tournaments, Teams, Team_Members
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

@studentsRouter.post('/tournament/join')
async def join_tournament(tournament_id: int, student_id: int, team_name: str, db: Session = Depends(get_db)):
    tournament_details = db.query(Tournaments).filter(Tournaments.id == tournament_id).first()
    student = db.query(Students).filter(Students.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Invalid student id")
    if tournament_details is None:
        raise HTTPException(status_code=404, detail="Invalid tournament id")
    
    team_obj = Teams(name=team_name, max_members_allowed=tournament_details.team_size,tournament_id=tournament_id,creator_id=student_id)
    db.add(team_obj)
    db.commit()
    db.refresh(team_obj)
    
    team_info = {
        "id": team_obj.id,
        "name": team_obj.name,
        "members_count": team_obj.members_count,
    }

    team_members = Team_Members(student_id = student_id, team_id=team_obj.id)
    db.add(team_members)
    db.commit()
    db.refresh(team_members)

    return team_info


