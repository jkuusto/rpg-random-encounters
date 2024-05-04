from app import app
from flask import (redirect, render_template, request, flash, url_for, 
                   jsonify, abort)
from users import *
from tables import *
from random import randint
import secrets

# Character limit for encounter descriptions
DESCRIPTION_CHAR_LIMIT = 2000


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard", methods=["GET"])
def dashboard():
    user_id_value = user_id()
    if not user_id_value:
        flash("You must be logged in to access the dashboard", "error")
        return redirect("/login")
    else:
        games = get_games(user_id_value)
        return render_template("dashboard.html", games=games)


@app.route("/game/<int:game_id>", methods=["GET"])
def game(game_id):
    game = get_game(game_id)
    if not game or game.user_id != user_id():
        flash("You don't have permission to access this page", "error")
        return redirect("/")
    else:
        encounter_types = get_encounter_types(game_id)
        biomes = get_biomes()
        encounters_general = get_encounters_general(game_id)
        encounters_biome = get_encounters_biome(game_id, game.biome_id)
        return render_template("game.html", 
                               game_id=game_id, 
                               game_name=game.name, 
                               encounter_types=encounter_types, 
                               biomes=biomes, 
                               current_biome_id=game.biome_id, 
                               encounters_general=encounters_general, 
                               encounters_biome=encounters_biome)


@app.route("/create_game", methods=["GET", "POST"])
def create_game():
    user_id_value = user_id()
    if not user_id_value:
        flash("You must be logged in to create a game", "error")
        return redirect("/login")
    else:
        if request.method == "POST":
            if session.get("csrf_token") != request.form.get("csrf_token"):
                abort(403)
            game_name = request.form["content"]
            if len(game_name) > 30:
                flash("Game name must be 30 characters or less", "error")
                return redirect("/dashboard")
            create_new_game(game_name, user_id_value)
            flash("Game created successfully", "success")
            return redirect("/dashboard")
        else:
            placeholder_text = "Enter game name here (max. 30 characters)"
            return render_template("edit_text.html", 
                                   placeholder=placeholder_text)


@app.route("/edit_text/<int:game_id>", methods=["GET", "POST"])
def rename_game(game_id):
    game = get_game(game_id)
    if not game or game.user_id != user_id():
        flash("You don't have permission to rename this game", "error")
        return redirect("/")
    else:
        if request.method == "POST":
            if session.get("csrf_token") != request.form.get("csrf_token"):
                abort(403)
            new_name = request.form["content"]
            if len(new_name) > 30:
                flash("Game name must be 30 characters or less", "error")
                return redirect("/dashboard")
            rename_game_db(game_id, new_name)
            flash("Game renamed successfully", "success")
            return redirect("/dashboard")
        else:
            placeholder_text = "Enter new name here (max. 30 characters)"
            return render_template("edit_text.html", game_id=game_id, 
                                   game_name=game.name, 
                                   placeholder=placeholder_text)


@app.route("/delete_game/<int:game_id>", methods=["POST"])
def delete_game(game_id):
    if session.get("csrf_token") != request.form.get("csrf_token"):
        abort(403)
    if game_id == 1:
        flash("This game cannot be deleted", "error")
    else:
        game = get_game(game_id)
        if not game or game.user_id != user_id():
            flash("You don't have permission to delete this game", "error")
        else:
            delete_game_db(game_id)
            flash("Game deleted successfully", "success")
    return redirect("/dashboard")


@app.route("/change_biome/<int:game_id>", methods=["POST"])
def change_biome(game_id):
    data = request.get_json()
    if session.get("csrf_token") != data.get("csrf_token"):
        abort(403)
    new_biome_id = request.json['biome_id']
    game = get_game(game_id)
    if not game or game.user_id != user_id():
        return "You don't have permission to change this game's biome", 403
    else:
        update_game_biome(game_id, new_biome_id)
        # return json to update the biome encounters table on game.html
        return jsonify(get_encounters_biome(game_id, new_biome_id))


@app.route("/change_roll_range/<int:game_id>", methods=["POST"])
def change_roll_range(game_id):
    data = request.get_json()
    if session.get("csrf_token") != data.get("csrf_token"):
        abort(403)
    data = request.get_json()
    id = data["id"]
    roll_range = data["roll_range"]
    table_name = data["table_name"]
    game = get_game(game_id)
    if not game or game.user_id != user_id():
        return "You don't have permission to change the roll range", 403
    try:
        roll_range = int(roll_range)
    except ValueError:
        return jsonify({"status": "error"})
    update_roll_range_db(id, roll_range, game_id, table_name)
    flash("Roll range updated successfully", "success")
    return jsonify({"status": "success"})


@app.route("/roll_type/<int:game_id>", methods=["POST"])
def roll_type(game_id):
    if session.get("csrf_token") != request.form.get("csrf_token"):
        abort(403)
    encounter_types = get_encounter_types(game_id)
    max_roll = int(encounter_types[-1][1].split('-')[1])
    roll_result = randint(1, max_roll)
    for id, roll_range, encounter_type in encounter_types:
        start_range, end_range = map(int, roll_range.split('-'))
        if start_range <= roll_result <= end_range:
            flash(f"Encounter type rolled ({roll_result}): {encounter_type}", 
                  "roll")
            # Make a successive roll for the encounter
            if encounter_type == "General encounter":
                encounters = get_encounters_general(game_id)
            else:  # Biome encounter
                game = get_game(game_id)
                encounters = get_encounters_biome(game_id, game.biome_id)
            roll_result, encounter = roll_encounter(encounters)
            flash(f"Encounter rolled ({roll_result}): {encounter}", "roll")
            break
    return redirect(url_for("game", game_id=game_id))


def roll_encounter(encounters):
    max_roll = int(encounters[-1][1].split('-')[1])
    roll_result = randint(1, max_roll)
    for id, roll_range, encounter in encounters:
        start_range, end_range = map(int, roll_range.split('-'))
        if start_range <= roll_result <= end_range:
            return roll_result, encounter


@app.route("/create_encounter/<string:encounter_type>/<int:game_id>", 
           methods=["GET", "POST"])
def create_encounter(encounter_type, game_id):
    game = get_game(game_id)
    if not game or game.user_id != user_id():
        flash("You don't have permission to create encounters here", "error")
        return redirect("/")
    else:
        if request.method == "POST":
            if session.get("csrf_token") != request.form.get("csrf_token"):
                abort(403)
            description = request.form["content"]
            if len(description) > DESCRIPTION_CHAR_LIMIT:
                flash(f"Description must be {DESCRIPTION_CHAR_LIMIT} "
                      f"characters or less", "error")
                return render_template("edit_text.html",  
                                    preset=description)
            if encounter_type == "general":
                insert_encounter_db("encounters_general", game_id, 
                                    description)
            elif encounter_type == "biome":
                biome_id = game.biome_id
                insert_encounter_db("encounters_biome", game_id, description, 
                                    biome_id=biome_id)
            flash("Encounter created successfully", "success")
            return redirect(url_for("game", game_id=game_id))
        else:
            placeholder_text = "Enter encounter description here"
            return render_template("edit_text.html", 
                                   placeholder=placeholder_text)


@app.route("/edit_encounter/<string:table_name>/<int:encounter_id>/"
           "<int:game_id>", methods=["GET", "POST"])
def rewrite_encounter(table_name, encounter_id, game_id):
    if request.method == "POST":
        if session.get("csrf_token") != request.form.get("csrf_token"):
            abort(403)
        new_description = request.form["content"]
        if len(new_description) > DESCRIPTION_CHAR_LIMIT:
            flash(f"Description must be {DESCRIPTION_CHAR_LIMIT} "
                  f"characters or less", "error")
            old_description = request.args.get("old_description", None)
            return render_template("edit_text.html", 
                                preset=new_description)
        update_encounter_description(table_name, encounter_id, 
                                     new_description)
        flash("Encounter description updated successfully", "success")
        return redirect(url_for("game", game_id=game_id))
    else:
        old_description = request.args.get("old_description", None)
        return render_template("edit_text.html", 
                               placeholder="Enter new description here", 
                               preset=old_description)


@app.route("/delete_encounter/<string:table_name>/<int:encounter_id>/"
           "<int:game_id>", methods=["POST"])
def delete_encounter(table_name, encounter_id, game_id):
    if session.get("csrf_token") != request.form.get("csrf_token"):
        abort(403)
    game = get_game(game_id)
    if not game or game.user_id != user_id():
        flash("You don't have permission to delete this encounter", "error")
    else:
        delete_encounter_db(table_name, encounter_id)
        flash("Encounter deleted successfully", "success")
    return redirect(url_for("game", game_id=game_id))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if login_user(username, password):
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("dashboard")
        else:
            flash("Invalid username or password", "error")
    return render_template("login.html")


@app.route("/logout")
def logout():
    if "csrf_token" in session:
        session.pop("csrf_token")
    logout_user()
    return redirect("/")


@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    if register_user(username, password):
        flash("Registration successful, you can login now", "success")
        return redirect("/login")
    else:
        flash("Registration failed", "error")
    return render_template("login.html")

