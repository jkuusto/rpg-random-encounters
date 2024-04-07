from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from db import db


def get_games(user_id):
    try:
        sql = text("SELECT id, name FROM games WHERE user_id=:user_id")
        result = db.session.execute(sql, {"user_id":user_id})
        return result.fetchall()
    except SQLAlchemyError as e:
        print("An error occured while fetching games from db", e)
        return []


def get_game(game_id):
    try:
        sql = text("SELECT user_id, name, biome_id FROM games WHERE id=:game_id")
        result = db.session.execute(sql, {"game_id":game_id})
        return result.fetchone()
    except SQLAlchemyError as e:
        print("An error occured while fetching a game from db", e)
        return None


def create_new_game(game_name, user_id):
    try:
        sql = text("INSERT INTO games (name, user_id, biome_id) VALUES (:name, :user_id, 1) RETURNING id")
        result = db.session.execute(sql, {"name":game_name, "user_id":user_id})
        game_id = result.fetchone()[0]
        db.session.commit()
        
        # Copy preset entries to the new game
        copy_preset_entries("main_probability", game_id, ["game_id", "encounter_type_id", "roll_range", "preset"])
        copy_preset_entries("encounters_general", game_id, ["game_id", "roll_range", "description", "preset"])
        copy_preset_entries("encounters_biome", game_id, ["game_id", "roll_range", "biome_id", "description", "preset"]) 
    except SQLAlchemyError as e:
        print("An error occured while creating new game", e)
        db.session.rollback()
        return None


def copy_preset_entries(table_name, game_id, columns):
    try:
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
    except SQLAlchemyError as e:
        print(f"An error occured copying preset entries to {table_name}", e)
        db.session.rollback()


def delete_game_from_db(game_id):
    try:
        sql = text("DELETE FROM games WHERE id=:game_id")
        db.session.execute(sql, {"game_id":game_id})
        db.session.commit()
    except SQLAlchemyError as e:
        print("An error occured while deleting a game from db", e)
        db.session.rollback()


def get_encounter_types(game_id):
    try:
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

        # Create a list of tuples with the roll range limits and encounter types
        ranges_with_types = []
        start_range = 1
        for encounter_type in encounter_types:
            end_range = start_range + encounter_type.roll_range - 1
            ranges_with_types.append((f"{start_range}-{end_range}", 
                                    encounter_type.name))
            start_range = end_range + 1
        return ranges_with_types
    except SQLAlchemyError as e:
        print("An error occured while fetching encounter types from db", e)
        return []


def get_biomes():
    try:
        sql = text("SELECT id, name FROM biomes ORDER BY id")
        result = db.session.execute(sql)
        return result.fetchall()
    except SQLAlchemyError as e:
        print("An error occured while fetching biomes from db", e)
        return []


def update_game_biome(game_id, new_biome_id):
    try:
        sql = text("UPDATE games SET biome_id = :biome_id WHERE id = :game_id")
        db.session.execute(sql, {"biome_id": new_biome_id, "game_id": game_id})
        db.session.commit()
    except SQLAlchemyError as e:
        print("An error occured while updating game biome", e)
        db.session.rollback()

