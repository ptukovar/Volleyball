from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class GamePlayer(Base):
    __tablename__ = "game_players"
    
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"))
    player_id = Column(Integer, ForeignKey("players.id"))
    team = Column(Integer, nullable=False)
    
    player = relationship("Player")
    game = relationship("Game")
    