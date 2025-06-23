from sqlalchemy import Column, Integer, DateTime
from datetime import datetime, timezone
from app.db.base import Base

class Game(Base):
    __tablename__ = "games"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)