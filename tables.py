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
        sql = text("""
                   SELECT user_id, name, biome_id 
                   FROM games 
                   WHERE id=:game_id
                   """)
        result = db.session.execute(sql, {"game_id":game_id})
        return result.fetchone()
    except SQLAlchemyError as e:
        print("An error occured while fetching a game from db", e)
        return None


def create_new_game(game_name, user_id):
    try:
        sql = text("""
                   INSERT INTO games (name, user_id, biome_id) 
                   VALUES (:name, :user_id, 1) RETURNING id""")
        result = db.session.execute(sql, 
                                    {"name":game_name, "user_id":user_id})
        game_id = result.fetchone()[0]
        db.session.commit()
        
        # Copy preset entries to the new game
        copy_preset_entries("main_probability", game_id, 
                            ["game_id", "encounter_type_id", 
                             "roll_range", "preset"])
        copy_preset_entries("encounters_general", game_id, 
                            ["game_id", "roll_range", 
                             "description", "preset"])
        copy_preset_entries("encounters_biome", game_id, 
                            ["game_id", "roll_range", 
                             "biome_id", "description", "preset"]) 
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


def rename_game_in_db(game_id, new_name):
    try:
        sql = text("UPDATE games SET name = :name WHERE id = :game_id")
        db.session.execute(sql, {"name": new_name, "game_id": game_id})
        db.session.commit()
    except SQLAlchemyError as e:
        print("An error occurred while renaming a game:", e)
        db.session.rollback()


def delete_game_from_db(game_id):
    try:
        sql = text("DELETE FROM games WHERE id=:game_id")
        db.session.execute(sql, {"game_id":game_id})
        db.session.commit()
    except SQLAlchemyError as e:
        print("An error occured while deleting a game from db", e)
        db.session.rollback()


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
        sql = text("""
                   UPDATE games 
                   SET biome_id = :biome_id 
                   WHERE id = :game_id""")
        db.session.execute(sql, 
                           {"biome_id": new_biome_id, "game_id": game_id})
        db.session.commit()
    except SQLAlchemyError as e:
        print("An error occured while updating game biome", e)
        db.session.rollback()


def get_encounter_data(sql_query, game_param):
    try:
        result = db.session.execute(sql_query, game_param)
        data = result.fetchall()

        # Create a list of tuples: (roll range limits, name/description) 
        ranges_with_data = []
        start_range = 1
        for encounter in data:
            end_range = start_range + encounter[1] - 1 # roll_range
            ranges_with_data.append((encounter[0], # id
                                     f"{start_range}-{end_range}", # formatted
                                     encounter[2])) # name or description
            start_range = end_range + 1
        return ranges_with_data
    except SQLAlchemyError as e:
        print("An error occured while fetching encounter data from db", e)
        return []


def get_encounter_types(game_id):
    sql = text("""
            SELECT main_probability.id, main_probability.roll_range, 
            encounter_types.name 
            FROM main_probability 
            JOIN encounter_types 
            ON main_probability.encounter_type_id = encounter_types.id 
            WHERE main_probability.game_id=:game_id 
            ORDER BY main_probability.roll_range DESC
            """)
    return get_encounter_data(sql, {"game_id":game_id})


def get_encounters_general(game_id):
    sql = text("""
            SELECT encounters_general.id, encounters_general.roll_range, 
            encounters_general.description 
            FROM encounters_general 
            WHERE encounters_general.game_id=:game_id 
            ORDER BY encounters_general.roll_range DESC
            """)
    return get_encounter_data(sql, {"game_id":game_id})


def get_encounters_biome(game_id, biome_id):
    sql = text("""
            SELECT encounters_biome.id, encounters_biome.roll_range, 
            encounters_biome.description 
            FROM encounters_biome 
            WHERE encounters_biome.game_id=:game_id 
            AND encounters_biome.biome_id=:biome_id 
            ORDER BY encounters_biome.roll_range DESC
            """)
    return get_encounter_data(sql, {"game_id":game_id, "biome_id":biome_id})


def update_roll_range_database(id, roll_range, game_id):
    try:
        sql = text("""
                   UPDATE main_probability 
                   SET roll_range = :roll_range 
                   WHERE id = :id 
                   AND game_id = :game_id
                   """)
        db.session.execute(sql, 
                           {"roll_range": roll_range, 
                            "id": id, 
                            "game_id": game_id})
        db.session.commit()
    except SQLAlchemyError as e:
        print("An error occured while updating roll range in database", e)
        db.session.rollback()
