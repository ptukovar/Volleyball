from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Player(Base):
    __tablename__="players"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    nickname = Column(String, nullable=False)
    role = Column(Integer, nullable=False)
    password = Column(String, nullable=False)
    image = Column(String, nullable=True)
