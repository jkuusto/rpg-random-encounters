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
        sql = text("SELECT name FROM games WHERE user_id=:user_id")
        result = db.session.execute(sql, {"user_id":user_id_value})
        games = result.fetchall()
        return render_template("dashboard.html", games=games)

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