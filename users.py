from db import db
from sqlalchemy.sql import text
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash


def login_user(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user or not check_password_hash(user.password, password):
        return False
    else:
        session["username"] = username
        session["user_id"] = user.id
        return True


def logout_user():
    del session["username"]
    del session["user_id"]


def register_user(username, password):
    # Check if username already exists
    sql = text("SELECT 1 FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username}).fetchone()
    if result:
        return None  # Username already exists

    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False


def user_id():
    return session.get("user_id",0)

