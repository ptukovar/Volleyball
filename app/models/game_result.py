from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class GameResult(Base):
    __tablename__ = "game_results"

    id           = Column(Integer, primary_key=True, index=True)
    game_id      = Column(Integer, ForeignKey("games.id"), nullable=False, unique=True)
    sets_team1   = Column(Integer, nullable=False)
    sets_team2   = Column(Integer, nullable=False)
    mvp          = Column(Integer, ForeignKey("players.id"), nullable=True)
    impostor     = Column(Integer, ForeignKey("players.id"), nullable=True)

    game         = relationship("Game",   back_populates="result")
