from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class GameSet(Base):
    __tablename__ = "game_sets"

    id          = Column(Integer, primary_key=True, index=True)
    game_id     = Column(Integer, ForeignKey("games.id"), nullable=False)
    set_number  = Column(Integer, nullable=False)
    team1_score = Column(Integer, nullable=False)
    team2_score = Column(Integer, nullable=False)

    game        = relationship("Game", back_populates="sets")
