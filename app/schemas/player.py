from typing import Optional
from pydantic import BaseModel

class PlayerBase(BaseModel):
    name: str
    image: Optional[str] = None
    
class PlayerCreate(PlayerBase):
    pass

class PlayerRead(PlayerBase):
    id: int
    
    model_config = {
        "from_attributes": True
    }