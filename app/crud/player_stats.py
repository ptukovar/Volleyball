from sqlalchemy.orm import Session
from sqlalchemy import func, case
from app.models.game_player import GamePlayer
from app.models.game_result import GameResult
from app.models.game_set import GameSet
from app.schemas.player_stats import PlayerStats


def get_player_stats(db: Session, player_id: int) -> PlayerStats:
    gp = db.query(GamePlayer).filter(GamePlayer.player_id == player_id).subquery()

    total_games = db.query(func.count()).select_from(gp).scalar() or 0

    wins = (db.query(func.count())
            .select_from(gp)
            .join(GameResult, GameResult.game_id == gp.c.game_id)
            .filter(
                case(
                    (gp.c.team == 1, GameResult.team1_score > GameResult.team2_score),
                    (gp.c.team == 2, GameResult.team2_score > GameResult.team1_score),
                    else_=False
                )
            )
            .scalar() or 0)

    losses = total_games - wins

    wins_team1 = (db.query(func.count())
                  .select_from(gp)
                  .join(GameResult, GameResult.game_id == gp.c.game_id)
                  .filter(gp.c.team == 1, GameResult.team1_score > GameResult.team2_score)
                  .scalar() or 0)
    wins_team2 = (db.query(func.count())
                  .select_from(gp)
                  .join(GameResult, GameResult.game_id == gp.c.game_id)
                  .filter(gp.c.team == 2, GameResult.team2_score > GameResult.team1_score)
                  .scalar() or 0)

    gs = (db.query(GameSet)
          .join(GamePlayer, GamePlayer.game_id == GameSet.game_id)
          .filter(GamePlayer.player_id == player_id)
          .subquery())

    total_sets = db.query(func.count()).select_from(gs).scalar() or 0

    sets_query = (db.query(GameSet, GamePlayer.team)
              .join(GamePlayer, (GamePlayer.game_id == GameSet.game_id) & (GamePlayer.player_id == player_id)))

    total_sets = sets_query.count()

    sets_won = sets_query.filter(
        case(
            (GameSet.team1_score > GameSet.team2_score, GamePlayer.team == 1),
            (GameSet.team2_score > GameSet.team1_score, GamePlayer.team == 2),
            else_=False
        )
    ).count()

    sets_lost = total_sets - sets_won

    records = (db.query(gp.c.team, GameResult.team1_score, GameResult.team2_score)
               .select_from(gp)
               .join(GameResult, GameResult.game_id == gp.c.game_id)
               .all())

    sum_for = 0
    sum_against = 0
    sum_wins = 0
    sum_losses = 0
    count_wins = 0
    count_losses = 0

    for team, score1, score2 in records:
        points_for = score1 if team == 1 else score2
        points_against = score2 if team == 1 else score1
        sum_for += points_for
        sum_against += points_against
        if points_for > points_against:
            sum_wins += points_for
            count_wins += 1
        else:
            sum_losses += points_for
            count_losses += 1

    avg_points = (sum_for / total_games) if total_games else 0.0
    avg_winning_points = (sum_wins / count_wins) if count_wins else 0.0
    avg_losing_points = (sum_losses / count_losses) if count_losses else 0.0

    mvp_count = (db.query(func.count())
                 .select_from(GameResult)
                 .filter(GameResult.mvp == player_id)
                 .scalar() or 0)
    impostor_count = (db.query(func.count())
                     .select_from(GameResult)
                     .filter(GameResult.impostor == player_id)
                     .scalar() or 0)

    return PlayerStats(
        total_games=total_games,
        wins=wins,
        losses=losses,
        win_rate=(wins / total_games)*100 if total_games else 0.0,
        wins_team1=wins_team1,
        wins_team2=wins_team2,
        total_sets=total_sets,
        sets_won=sets_won,
        sets_lost=sets_lost,
        sets_win_rate=(sets_won / total_sets)*100 if total_sets else 0.0,
        avg_points=avg_points,
        avg_winning_points=avg_winning_points,
        avg_losing_points=avg_losing_points,
        mvp_count=mvp_count,
        impostor_count=impostor_count
    )