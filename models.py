# models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Association table for many-to-many relationship between events and games
event_game_association = Table(
    'event_game', Base.metadata,
    Column('event_id', Integer, ForeignKey('events.id')),
    Column('game_id', Integer, ForeignKey('games.id'))
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String, unique=True, nullable=False)
    username = Column(String)
    role = Column(String, default='player')  # 'admin' or 'player'
    favorite_games = relationship('Game', secondary='user_game', back_populates='liked_by')

class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    image_path = Column(String)
    max_players = Column(Integer)
    liked_by = relationship('User', secondary='user_game', back_populates='favorite_games')

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    date_time = Column(DateTime, nullable=False)
    games = relationship('Game', secondary=event_game_association, back_populates='events')
    participants = relationship('User', secondary='event_user', back_populates='events')

# Association table for many-to-many relationship between users and games
user_game_association = Table(
    'user_game', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('game_id', Integer, ForeignKey('games.id'))
)

# Association table for many-to-many relationship between users and events
event_user_association = Table(
    'event_user', Base.metadata,
    Column('event_id', Integer, ForeignKey('events.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)