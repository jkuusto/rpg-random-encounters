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

def create_new_game(game_name, user_id):
    sql = text("INSERT INTO games (name, user_id, biome_id) VALUES (:name, :user_id, 1) RETURNING id")
    result = db.session.execute(sql, {"name":game_name, "user_id":user_id})
    game_id = result.fetchone()[0]
    db.session.commit()
    
    # Copy preset entries to the new game
    copy_preset_entries("main_probability", game_id, ["game_id", "encounter_type_id", "roll_range", "preset"])
    copy_preset_entries("encounters_general", game_id, ["game_id", "roll_range", "description", "preset"])
    copy_preset_entries("encounters_biome", game_id, ["game_id", "roll_range", "biome_id", "description", "preset"]) 

def copy_preset_entries(table_name, game_id, columns):
    column_values = columns.copy()
    column_values.remove("game_id")
    column_values[column_values.index("preset")] = "false"
    
    columns_str = ", ".join(columns)
    column_values_str = ", ".join(column_values)
    
    sql = text(f"""
               INSERT INTO {table_name} ({columns_str})
               SELECT :game_id, {column_values_str}
               FROM {table_name}
               WHERE preset=true
               """)
    db.session.execute(sql, {"game_id":game_id})
    db.session.commit()