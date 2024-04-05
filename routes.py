from app import app
from flask import redirect, render_template, request, flash
from users import *

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
        sql = text("SELECT id, name FROM games WHERE user_id=:user_id")
        result = db.session.execute(sql, {"user_id":user_id_value})
        games = result.fetchall()
        return render_template("dashboard.html", games=games)
    
@app.route("/game/<int:game_id>", methods=["GET"])
def game(game_id):
    sql = text("SELECT user_id, name FROM games WHERE id=:game_id")
    result = db.session.execute(sql, {"game_id":game_id})
    game = result.fetchone()
    if not game or game.user_id != user_id():
        flash("You don't have permission to access this page", "error")
        return redirect("/")
    else:
        sql = text("""
                   SELECT encounter_types.name 
                   FROM main_probability 
                   JOIN encounter_types 
                   ON main_probability.encounter_type_id = encounter_types.id 
                   WHERE main_probability.game_id=:game_id
                   """)
        result = db.session.execute(sql, {"game_id":game_id})
        encounter_types = result.fetchall()
        return render_template("game.html", game_name=game.name, encounter_types=encounter_types)

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