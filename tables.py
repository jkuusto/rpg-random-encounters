from sqlalchemy import text
from db import db

def get_games(user_id):
    sql = text("SELECT id, name FROM games WHERE user_id=:user_id")
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def get_game(game_id):
    sql = text("SELECT user_id, name FROM games WHERE id=:game_id")
    result = db.session.execute(sql, {"game_id":game_id})
    return result.fetchone()

def get_encounter_types(game_id):
    sql = text("""
               SELECT main_probability.roll_range, encounter_types.name 
               FROM main_probability 
               JOIN encounter_types 
               ON main_probability.encounter_type_id = encounter_types.id 
               WHERE main_probability.game_id=:game_id 
               ORDER BY main_probability.roll_range DESC
               """)
    result = db.session.execute(sql, {"game_id":game_id})
    encounter_types = result.fetchall()
    ranges_with_types = []
    start_range = 1
    for encounter_type in encounter_types:
        end_range = start_range + encounter_type.roll_range - 1
        ranges_with_types.append((f"{start_range}-{end_range}", 
                                  encounter_type.name))
        start_range = end_range + 1
    return ranges_with_types