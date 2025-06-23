from datetime import datetime
from pydantic import BaseModel

class GameBase(BaseModel):
    date: datetime
    
class GameCreate(GameBase):
    pass

class GameRead(GameBase):
    id: int
    
    model_config = {
        "from_attributes": True
    }