

from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import relationship
import datetime

from config.db import Base
    
class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True,index=True)
    name = Column(String(80), nullable=False)
    email= Column(String(80), nullable=False, unique=True)
    def __repr__(self):
        return 'ItemModel(name=%s)' % (self.name)
    
class Students(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    email = Column(String(80), nullable=False)
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return 'ItemModel(name=%s)' % (self.name)

class Games(Base):
    __tablename__ = "games"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False)

    def __repr__(self):
        return 'ItemModel(name=%s)' % (self.name)

class Organizers(Base):
    __tablename__ = "organizers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False)
    email = Column(String(80), nullable=False)
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)

class Tournaments(Base):
    __tablename__ = "tournaments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(String(500), nullable=True, default="")
    team_size = Column(Integer)
    max_teams = Column(Integer)
    total_matches = Column(Integer)
    isActive = Column(Boolean, default=True)
    organizer_id = Column(Integer, ForeignKey("organizers.id", ondelete="CASCADE"), nullable=False)
    organizer = relationship("Organizers")
    game_id = Column(Integer, ForeignKey("games.id", ondelete="CASCADE"), nullable=False)
    game = relationship("Games")
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)

class Teams(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False)
    members_count = Column(Integer, default=1)
    max_members_allowed = Column(Integer, default=1)
    tournament_id = Column(Integer, ForeignKey("tournaments.id", ondelete="CASCADE"), nullable=False)
    tournament = relationship("Tournaments")
    creator_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    creator = relationship("Students")
    team_members = relationship("Team_Members", back_populates="team")
    isApproved = Column(Boolean, default=False)
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)

class Team_Members(Base):
    __tablename__ = "team_members"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    student = relationship("Students")
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    team = relationship("Teams", back_populates="team_members")
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    

class Matches(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True, index=True)
    team_id1 = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    team_1 = relationship("Teams", foreign_keys=[team_id1])
    team_id2 = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    team_2 = relationship("Teams", foreign_keys=[team_id2])
    winner_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), nullable=True)
    winner = relationship("Teams", foreign_keys=[winner_id])
    tournament_id =  Column(Integer, ForeignKey("tournaments.id", ondelete="CASCADE"), nullable=False)
    tournament = relationship("Tournaments")
    round_number = Column(Integer, default=1, nullable=False)
    date = Column(DateTime, nullable=False)
    
class Scores(Base):
    __tablename__ = "scores"
    id = Column(Integer, primary_key=True, index=True)
    team1_score = Column(Integer)
    team2_score = Column(Integer)
    match_id = Column(Integer, ForeignKey("matches.id", ondelete="CASCADE"), nullable=False)
    match = relationship("Matches")

class Rounds(Base):
    __tablename__ = "rounds"
    id = Column(Integer, primary_key=True, index=True)
    tournament_id =  Column(Integer, ForeignKey("tournaments.id", ondelete="CASCADE"), nullable=False)
    tournament = relationship("Tournaments")
    round_no = Column(Integer, default=1, nullable=False)
    no_teams = Column(Integer, nullable=False)
    no_matches = Column(Integer, default=1, nullable=False)

# class Knockouts(Base):
#     __tablename__ = "knockouts"
#     id = Column(Integer, primary_key=True, index=True)
#     tournament_id =  Column(Integer, ForeignKey("tournaments.id", ondelete="CASCADE"), nullable=False)
#     tournament = relationship("Tournaments")
#     team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
#     team = relationship("Teams")
#     position = Column(Integer)
#     stage = Column(Integer)

