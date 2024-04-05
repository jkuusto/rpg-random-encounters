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
               SELECT encounter_types.name 
               FROM main_probability 
               JOIN encounter_types 
               ON main_probability.encounter_type_id = encounter_types.id 
               WHERE main_probability.game_id=:game_id
               """)
    result = db.session.execute(sql, {"game_id":game_id})
    return result.fetchall()