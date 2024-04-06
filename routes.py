from app import app
from flask import redirect, render_template, request, flash
from users import *
from tables import *

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
        return render_template("game.html", game_name=game.name, encounter_types=encounter_types)
    
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