from sqlalchemy.orm import Session
from app.models.game_player import GamePlayer
from app.schemas.game_player import GamePlayerCreate

def add_player_to_game(db: Session, game_id: int, game_player: GamePlayerCreate) -> GamePlayer:
    db_game_player = GamePlayer(**game_player.model_dump(), game_id=game_id)
    db.add(db_game_player)
    db.commit()
    db.refresh(db_game_player)
    return db_game_player