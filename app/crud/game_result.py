from sqlalchemy.orm import Session
from app.models.game_result import GameResult
from app.schemas.game_result import GameResultCreate

def set_game_result(db: Session, game_id: int, game_result: GameResultCreate) -> GameResult:
    db_game_result = GameResult(**game_result.dict(), game_id=game_id)
    db.add(db_game_result)
    db.commit()
    db.refresh(db_game_result)
    return db_game_result