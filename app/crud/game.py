from sqlalchemy.orm import Session
from app.models.game import Game
from app.schemas.game import GameCreate

def create_game(db: Session, game: GameCreate) -> Game:
    db_game = Game(**game.dict())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

def get_game(db: Session, game_id: int) -> Game:
    return db.query(Game).filter(Game.id == game_id).first()
