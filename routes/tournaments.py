from fastapi import APIRouter, HTTPException, Request
from models.index import Tournaments, Games, Organizers
from schemas.index import Tournament
from sqlalchemy.orm import Session, joinedload
from fastapi import Depends
from config.db import get_db

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
    tournament = db.query(Tournaments).filter(Tournaments.id == id).first()
    if tournament is None:
        raise HTTPException(status_code=404, detail="tournament not found")
    return tournament


