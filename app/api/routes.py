from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.player import PlayerCreate, PlayerRead
from app.schemas.game import GameCreate, GameRead
from app.schemas.game_result import GameResultCreate, GameResultRead
from app.schemas.game_player import GamePlayerCreate, GamePlayerRead
from app.schemas.player_stats import PlayerStats

import app.crud.player as player_crud
import app.crud.game as game_crud
import app.crud.game_result as game_result_crud
import app.crud.game_player as game_player_crud

api_router = APIRouter()

@api_router.post("/players/", response_model=PlayerRead)
def create_player(player: PlayerCreate, db: Session = Depends(get_db)):
    return player_crud.create_player(db=db, player=player)

@api_router.get("/players/{player_id}", response_model=PlayerRead)
def read_player(player_id: int, db: Session = Depends(get_db)):
    db_player = player_crud.get_player(db=db, player_id=player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return db_player

@api_router.post("/games/", response_model=GameRead)
def create_game(game: GameCreate, db: Session = Depends(get_db)):
    return game_crud.create_game(db=db, game=game)

@api_router.get("/games/{game_id}", response_model=GameRead)
def read_game(game_id: int, db: Session = Depends(get_db)):
    db_game = game_crud.get_game(db=db, game_id=game_id)
    if db_game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return db_game

@api_router.post("/games/{game_id}/players", response_model=GamePlayerRead)
def add_player(game_id: int, gp: GamePlayerCreate, db: Session = Depends(get_db)):
    return game_player_crud.add_player_to_game(db=db, game_id=game_id, game_player=gp)

@api_router.post("/games/{game_id}/result", response_model=GameResultRead)
def set_result(game_id: int, result: GameResultCreate, db: Session = Depends(get_db)):
    return game_result_crud.set_game_result(db=db, game_id=game_id, game_result=result)

@api_router.get("players/{player_id}/stats", response_model=PlayerStats)
def read_player_stats(player_id: int, db: Session = Depends(get_db)):
    if not player_crud.get_player(db, player_id):
        raise HTTPException(status_code=404, detail="Player not found")
    stats = player_crud.get_player_stats(db, player_id)
    return stats

