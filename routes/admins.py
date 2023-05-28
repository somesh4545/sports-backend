from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from models.index import Games, Tournaments, Organizers, Matches
from schemas.index import Game
from sqlalchemy.orm import Session, joinedload, load_only
from fastapi import Depends
from config.db import get_db

adminsRouter = APIRouter()

@adminsRouter.get('/game')
async def fetch_all_games(db: Session = Depends(get_db)):
    return db.query(Games).all()

@adminsRouter.post('/game')
async def add_new_game(game: Game, db: Session = Depends(get_db)):
    game_item = Games(name=game.name)
    db.add(game_item)
    db.commit()
    db.refresh(game_item)
    return game_item

@adminsRouter.get('/tournaments')
async def get_latest_tournaments(db: Session = Depends(get_db)):
    tournament = db.query(Tournaments).options(
        joinedload(Tournaments.organizer).load_only(Organizers.name)
    ).filter(Tournaments.isActive==True).order_by(Tournaments.start_date.desc()).all()

    result = []

    for t in tournament:
        count = db.query(Matches).filter(Matches.tournament_id==t.id, Matches.winner_id!=None).count()
        obj = {
            "tournament_id": t.id,
            "total_matches": t.total_matches,
            "matches_played": count,
            "organizer": t.organizer.name 
        }
        result.append(obj)


    return result
