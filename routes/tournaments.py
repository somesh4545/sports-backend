from fastapi import APIRouter, HTTPException, Request
from models.index import Tournaments, Games, Organizers, Teams, Students, Team_Members, Matches, Rounds, Scores
from schemas.index import Tournament, Score
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

@tournamentsRouter.post('/{id}/fixtures')
async def create_tournament_fixtures(id, db: Session = Depends(get_db)):
    teams = db.query(Teams).options(load_only(Teams.name)).filter(Teams.tournament_id==id, Teams.isApproved==True).order_by(Teams.name.asc()).all()

    if teams is None:
        raise HTTPException(status_code=404, detail="entries not found")

    check = db.query(Matches).filter(or_(Matches.team_id1==teams[0].id, Matches.team_id2==teams[0].id)).count()
    if check > 0:
        raise HTTPException(status_code=404, detail="fixtures already created")

    for i in range(0, len(teams), 2):
        team_id1 = teams[i].id
        team_id2 = teams[i+1].id

        match = Matches(team_id1=team_id1, team_id2=team_id2, winner=None, tournament_id=id, round_number=1, date=datetime.datetime.now())
        db.add(match)
        db.commit()

    round = Rounds(tournament_id=id, round_no=1, no_teams=len(teams), no_matches=len(teams)/2)
    db.add(round)
    db.commit()

    return {"msg": "fixtures created successfully"}

@tournamentsRouter.get('{id}/fixtures')
async def get_tournament_fixtures(id, db: Session = Depends(get_db)):
    matches = db.query(Matches).filter(Matches.tournament_id==id).order_by(Matches.round_number.desc()).all()

    if matches is None:
        raise HTTPException(status_code=404, detail="fixtures not found")
    
    return matches

@tournamentsRouter.post('{id}/match/{match_id}')
async def match_result(id, match_id, winner_id: int, db: Session=Depends(get_db)):
    match = db.query(Matches).filter(Matches.id == match_id).first()

    if match is None:
        raise HTTPException(status_code=404, detail="match not found")
    
    match.winner_id = winner_id
    db.commit()

    round = db.query(Rounds).filter(Rounds.tournament_id==id).first()
    count_of_matches_completed = db.query(Matches).filter(Matches.tournament_id==id, Matches.winner_id!=None, Matches.round_number==round.round_no).count()
    if count_of_matches_completed == round.no_matches and round.no_matches!=1:
        teams_available = round.no_teams
        
        if teams_available >= 2:
            teams = db.query(Matches).options(load_only(Matches.winner_id)).filter(Matches.tournament_id==id, Matches.round_number==round.round_no).all()
            for i in range(0, len(teams), 2):
                team_id1 = teams[i].winner_id
                team_id2 = teams[i+1].winner_id

                match = Matches(team_id1=team_id1, team_id2=team_id2,winner=None, tournament_id=id, round_number=round.round_no+1,date=datetime.datetime.now())
                
                db.add(match)
                db.commit()

        round.no_matches = round.no_matches/2
        round.no_teams = round.no_teams/2
        round.round_no = round.round_no+1

        db.commit()

@tournamentsRouter.get('{id}/match/{match_id}/score')
async def get_match_score(id, match_id, db: Session=Depends(get_db)):
    score = db.query(Scores).options(joinedload(Scores.match)).filter(Scores.match_id==match_id).first()
    if score is None:
        raise HTTPException(status_code=404, detail="score not found")
    return score

@tournamentsRouter.post('{id}/match/{match_id}/score')
async def post_match_score(id, match_id,scores: Score, db: Session=Depends(get_db)):
    score_obj = Scores(**scores.dict())

    db.add(score_obj)
    db.commit()
    db.refresh(score_obj)
    
    return score_obj




    