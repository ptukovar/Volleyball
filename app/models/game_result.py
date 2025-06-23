from sqlalchemy import Column, Integer, ForeignKey
from app.db.base import Base

class GameResult(Base):
    __tablename__ = "game_results"
    
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    team1_score = Column(Integer, nullable=False)
    team2_score = Column(Integer, nullable=False)
    