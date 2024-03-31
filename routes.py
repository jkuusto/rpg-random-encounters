from app import app
from flask import redirect, render_template, request, flash
from users import *

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if not login_user(username, password):
        flash("Invalid username or password", "error")
    return redirect("/")

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    if register_user(username, password):
        flash("Registration successful", "success")
    else:
        flash("Registration failed", "error")
    return redirect("/")