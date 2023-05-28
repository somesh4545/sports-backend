from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from models.index import Students, Tournaments, Teams, Team_Members
from schemas.index import Student
from sqlalchemy.orm import Session , joinedload
from fastapi import Depends
from config.db import get_db

teamsRouter = APIRouter()

@teamsRouter.get('/{id}')
async def get_team_by_id(id, db: Session = Depends(get_db)):
    team = db.query(Teams).options(
        joinedload(Teams.creator).load_only(Students.name, Students.email),
        joinedload(Teams.team_members).load_only(Team_Members.id).joinedload(Team_Members.student).load_only(Students.name, Students.email)
    ).filter(Teams.id==id).first()
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")

    return team

