from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_
from app.models.player import Player
from app.models.game_player import GamePlayer
from app.models.game_result import GameResult
from app.models.game_set import GameSet
from app.schemas.player import PlayerCreate
from app.schemas.player_stats import PlayerStats

def create_player(db: Session, player: PlayerCreate) -> Player:
    db_player = Player(**player.dict())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

def get_players(db: Session, skip: int = 0, limit: int = 100) -> list[Player]:
    return db.query(Player).offset(skip).limit(limit).all()

def get_player(db: Session, player_id: int) -> Player:
    return db.query(Player).filter(Player.id == player_id).first()


def get_player_stats(db: Session, player_id: int) -> PlayerStats:
    gp = db.query(GamePlayer).filter(GamePlayer.player_id == player_id).subquery()
    total_games = db.query(func.count()).select_from(gp).scalar() or 0

    wins = (
        db.query(func.count())
          .select_from(gp)
          .join(GameResult, GameResult.game_id == gp.c.game_id)
          .filter(
              or_(
                  and_(gp.c.team == 1, GameResult.sets_team1 > GameResult.sets_team2),
                  and_(gp.c.team == 2, GameResult.sets_team2 > GameResult.sets_team1),
              )
          )
          .scalar()
        or 0
    )
    losses = total_games - wins

    wins_team1 = (
        db.query(func.count())
          .select_from(gp)
          .join(GameResult, GameResult.game_id == gp.c.game_id)
          .filter(gp.c.team == 1, GameResult.sets_team1 > GameResult.sets_team2)
          .scalar()
        or 0
    )
    wins_team2 = (
        db.query(func.count())
          .select_from(gp)
          .join(GameResult, GameResult.game_id == gp.c.game_id)
          .filter(gp.c.team == 2, GameResult.sets_team2 > GameResult.sets_team1)
          .scalar()
        or 0
    )

    total_sets = (
        db.query(func.count())
          .select_from(GameSet)
          .join(GamePlayer, and_(
              GamePlayer.game_id == GameSet.game_id,
              GamePlayer.player_id == player_id
          ))
          .scalar()
        or 0
    )

    sets_won = (
        db.query(func.count())
          .select_from(GameSet)
          .join(GamePlayer, and_(
              GamePlayer.game_id == GameSet.game_id,
              GamePlayer.player_id == player_id
          ))
          .filter(
              or_(
                  and_(GamePlayer.team == 1, GameSet.team1_score > GameSet.team2_score),
                  and_(GamePlayer.team == 2, GameSet.team2_score > GameSet.team1_score),
              )
          )
          .scalar()
        or 0
    )
    sets_lost = total_sets - sets_won

    records = (
        db.query(
            gp.c.team,
            GameSet.team1_score,
            GameSet.team2_score
        )
        .select_from(gp)
        .join(GameSet, GameSet.game_id == gp.c.game_id)
        .all()
    )
    sum_for = sum((score1 if team == 1 else score2) for team, score1, score2 in records)
    wins_scores = [
        (score1 if team == 1 else score2)
        for team, score1, score2 in records
        if (score1 if team == 1 else score2) > (score2 if team == 1 else score1)
    ]
    losses_scores = [
        (score1 if team == 1 else score2)
        for team, score1, score2 in records
        if (score1 if team == 1 else score2) <= (score2 if team == 1 else score1)
   ]

    avg_points = (sum_for / total_games) if total_games else 0.0
    avg_winning_points = (sum(wins_scores) / len(wins_scores)) if wins_scores else 0.0
    avg_losing_points = (sum(losses_scores) / len(losses_scores)) if losses_scores else 0.0

    mvp_count = (
        db.query(func.count())
          .select_from(GameResult)
          .filter(GameResult.mvp == player_id)
          .scalar()
        or 0
    )
    impostor_count = (
        db.query(func.count())
          .select_from(GameResult)
          .filter(GameResult.impostor == player_id)
          .scalar()
        or 0
    )

    return PlayerStats(
        total_games=total_games,
        wins=wins,
        losses=losses,
        win_rate=(wins / total_games) * 100 if total_games else 0.0,
        wins_team1=wins_team1,
        wins_team2=wins_team2,
        total_sets=total_sets,
        sets_won=sets_won,
        sets_lost=sets_lost,
        sets_win_rate=(sets_won / total_sets) * 100 if total_sets else 0.0,
        avg_points=avg_points,
        avg_winning_points=avg_winning_points,
        avg_losing_points=avg_losing_points,
        mvp_count=mvp_count,
        impostor_count=impostor_count
    )
