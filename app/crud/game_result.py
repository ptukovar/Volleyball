from sqlalchemy.orm import Session
from app.models.game_result import GameResult
from app.schemas.game_result import GameResultCreate

from fastapi import HTTPException
from app import models

def set_game_result(db: Session, game_id: int, game_result: GameResultCreate) -> models.GameResult:
    game_players = db.query(models.GamePlayer).filter_by(game_id=game_id).all()
    player_ids = {gp.player_id for gp in game_players}

    for pid, role in [(game_result.mvp, "MVP"), (game_result.impostor, "Impostor")]:
        if pid is not None and pid not in player_ids:
            raise HTTPException(
                status_code=400,
                detail=f"{role} (player_id={pid}) did not participate in this game"
            )

    existing = db.query(models.GameResult).filter_by(game_id=game_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Result already exists for this game")

    db_result = models.GameResult(
        game_id=game_id,
        sets_team1=game_result.sets_team1,
        sets_team2=game_result.sets_team2,
        mvp=game_result.mvp,
        impostor=game_result.impostor
    )
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result


def get_game_result(db: Session, game_id: int) -> GameResult:
    return db.query(GameResult).filter(GameResult.game_id == game_id).first()