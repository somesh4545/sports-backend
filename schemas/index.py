from pydantic import BaseModel
import datetime

class User(BaseModel):
    name: str
    email: str

class Student(BaseModel):
    name: str
    email: str
    
class Games(BaseModel):
    name: str

class Organizer(BaseModel):
    name: str
    email: str

class Tournament(BaseModel):
    name: str
    description: str
    team_size: int
    max_teams: int
    total_matches: int
    isActive: bool
    organizer_id: int
    game_id: int
    start_date: datetime.datetime
    end_date: datetime.datetime

class Teams(BaseModel):
    name: str
    members_count : int
    max_members_allowed: int
    tournament_id: int
    creator_id: int

class Team_Members(BaseModel):
    student_id: int
    team_id: int

class Registrations(BaseModel):
    team_id: int
    tournament_id: int
    isApproved: bool
    
class Matches(BaseModel):
    team_id1: int
    team_id2 : int
    winner_id: int
    date: datetime.datetime
    
class Scores(BaseModel):
    team1_score: int
    team2_score: int
    match_id: int

class Knockouts(BaseModel):
    tournament_id: int
    team_id: int
    position: int
    stage: int

