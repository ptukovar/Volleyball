from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base

class Game(Base):
    __tablename__ = "games"

    id   = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    players = relationship("GamePlayer", back_populates="game", cascade="all, delete-orphan")
    sets    = relationship("GameSet",    back_populates="game", cascade="all, delete-orphan")
    result  = relationship("GameResult", back_populates="game", uselist=False)
