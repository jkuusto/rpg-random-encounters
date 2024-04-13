from app import app
from flask import redirect, render_template, request, flash, url_for, jsonify
from users import *
from tables import *
from random import randint


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


@app.route("/create_game", methods=["POST"])
def create_game():
    game_name = request.form["name"]
    user_id_value = user_id()
    if not user_id_value:
        flash("You must be logged in to create a game", "error")
        return redirect("/login")
    else:
        create_new_game(game_name, user_id_value)
        flash("Game created successfully", "success")
        return redirect("/dashboard")

@app.route("/edit_text/<int:game_id>", methods=["GET", "POST"])
def rename_game(game_id):
    game = get_game(game_id)
    if not game or game.user_id != user_id():
        flash("You don't have permission to rename this game", "error")
        return redirect("/")
    else:
        if request.method == "POST":
            new_name = request.form["name"]
            rename_game_in_db(game_id, new_name)
            flash("Game renamed successfully", "success")
            return redirect("/dashboard")
        else:
            return render_template("edit_text.html", game_id=game_id, game_name=game.name)

@app.route("/delete_game/<int:game_id>", methods=["POST"])
def delete_game(game_id):
    if game_id == 1:
        flash("This game cannot be deleted", "error")
    else:
        game = get_game(game_id)
        if not game or game.user_id != user_id():
            flash("You don't have permission to delete this game", "error")
        else:
            delete_game_from_db(game_id)
            flash("Game deleted successfully", "success")
    return redirect("/dashboard")


@app.route("/change_biome/<int:game_id>", methods=["POST"])
def change_biome(game_id):
    new_biome_id = request.json['biome_id']
    game = get_game(game_id)
    if not game or game.user_id != user_id():
        return "You don't have permission to change this game's biome", 403
    else:
        update_game_biome(game_id, new_biome_id)
        # return json to update the biome encounters table on game.html
        return jsonify(get_encounters_biome(game_id, new_biome_id))


@app.route("/roll_type/<int:game_id>", methods=["POST"])
def roll_type(game_id):
    encounter_types = get_encounter_types(game_id)
    max_roll = int(encounter_types[-1][0].split('-')[1])
    roll_result = randint(1, max_roll)
    for roll_range, encounter_type in encounter_types:
        start_range, end_range = map(int, roll_range.split('-'))
        if start_range <= roll_result <= end_range:
            flash(f"Encounter type rolled ({roll_result}): {encounter_type}", 
                  "success")
            break
    return redirect(url_for('game', game_id=game_id))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if login_user(username, password):
            return redirect("dashboard")
        else:
            flash("Invalid username or password", "error")
    return render_template("login.html")


@app.route("/logout")
def logout():
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

