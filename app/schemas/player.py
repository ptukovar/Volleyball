from pydantic import BaseModel

class PlayerBase(BaseModel):
    first_name: str
    last_name: str
    nickname: str
    role: int
    password: str
    image: str
    
class PlayerCreate(PlayerBase):
    pass

class PlayerRead(PlayerBase):
    id: int
    
    class Config:
        orm_mode = True