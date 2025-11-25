from sqlalchemy.orm import Session
from app.models.game_set import GameSet
from app.schemas.game_set import GameSetCreate

def create_game_set(db: Session, game_id: int, gs: GameSetCreate) -> GameSet:
    db_set = GameSet(
        game_id=game_id,
        set_number=gs.set_number,
        team1_score=gs.team1_score,
        team2_score=gs.team2_score
    )
    db.add(db_set)
    db.commit()
    db.refresh(db_set)
    return db_set

def get_sets_for_game(db: Session, game_id: int):
    return db.query(GameSet).filter(GameSet.game_id == game_id).order_by(GameSet.set_number).all()
