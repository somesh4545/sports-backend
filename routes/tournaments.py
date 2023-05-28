from fastapi import APIRouter, HTTPException, Request
from models.index import Tournaments, Games, Organizers, Teams, Students, Team_Members, Matches
from schemas.index import Tournament
from sqlalchemy.orm import Session, joinedload, load_only
from sqlalchemy import or_
from fastapi import Depends
from config.db import get_db
import datetime

tournamentsRouter = APIRouter()

@tournamentsRouter.get('/')
async def fetch_all_tournaments(request: Request, db: Session = Depends(get_db), isActive: bool = True):
    tournaments = db.query(Tournaments).options(
        joinedload(Tournaments.game).load_only(Games.name), 
        joinedload(Tournaments.organizer).load_only(Organizers.name)).where(Tournaments.isActive==isActive).all()

    # Access the game and organizer fields for each tournament
    for tournament in tournaments:
        game = tournament.game.name
        organizer = tournament.organizer.name
        # Perform any necessary operations with the game and organizer data

    # Return the tournaments with game and organizer populated
    return tournaments

@tournamentsRouter.post('/')
async def create_tournament(tournament: Tournament, db: Session = Depends(get_db)):
    tournament_item = Tournaments(**tournament.dict())
    db.add(tournament_item)
    db.commit()
    db.refresh(tournament_item)
    return tournament_item

@tournamentsRouter.get('/{id}')
async def get_by_id(id, db: Session = Depends(get_db)):
    tournament = db.query(Tournaments).options(
        joinedload(Tournaments.game).load_only(Games.name),
         joinedload(Tournaments.organizer).load_only(Organizers.name)
    ).filter(Tournaments.id == id).first()
    if tournament is None:
        raise HTTPException(status_code=404, detail="tournament not found")
    return tournament

@tournamentsRouter.get('/{id}/entries')
async def get_entries(id, isApproved: bool = None, db: Session = Depends(get_db)):
    team = db.query(Teams).options(
        joinedload(Teams.creator).load_only(Students.name, Students.email),
        joinedload(Teams.team_members).load_only(Team_Members.id).joinedload(Team_Members.student).load_only(Students.name, Students.email)
    ).filter(Teams.tournament_id==id)

    if isApproved is not None:
        team = team.filter(Teams.isApproved==isApproved)
    
    team = team.all()

    if team is None:
        raise HTTPException(status_code=404, detail="entries not found")
    
    return team

@tournamentsRouter.post('/{id}/create_fixtures')
async def create_match_fixtures(id, db: Session = Depends(get_db)):
    teams = db.query(Teams).options(load_only(Teams.name)).filter(Teams.tournament_id==id, Teams.isApproved==True).order_by(Teams.name.asc()).all()

    if teams is None:
        raise HTTPException(status_code=404, detail="entries not found")

    check = db.query(Matches).filter(or_(Matches.team_id1==teams[0].id, Matches.team_id2==teams[0].id)).count()
    if check > 0:
        raise HTTPException(status_code=404, detail="fixtures already created")

    for i in range(0, len(teams), 2):
        team_id1 = teams[i].id
        team_id2 = teams[i+1].id

        match = Matches(team_id1=team_id1, team_id2=team_id2,winner=None,date=datetime.datetime.now())
        db.add(match)
        db.commit()

    return {"msg": "fixtures created successfully"}

