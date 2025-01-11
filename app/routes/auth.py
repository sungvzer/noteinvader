from flask import Blueprint, redirect, render_template, url_for, request
from flask_login import current_user, login_user, login_required, logout_user
import bcrypt

from app.forms.auth import LoginForm, SignupForm
from app.models.user import User
from app.utils.db import get_db

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    db = get_db()
    if current_user.is_authenticated:
        return redirect(url_for("templates.index"))

    form = LoginForm()
    if form.validate_on_submit():  # Check if the form has been submitted
        email_or_username = form.email_or_username.data
        password = form.password.data
        if email_or_username is None or password is None:
            form.form_errors.append("Invalid login or password")
            return render_template("auth/login.html", form=form)

        # Check if the user exists in the database
        user = db.users.find_one(
            {"$or": [{"email": email_or_username}, {"username": email_or_username}]}
        )
        if user is None:
            form.form_errors.append("Invalid login or password")
            return render_template("auth/login.html", form=form)

        # Check if the password is correct
        hashed = user["password"]
        if not bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8")):
            form.form_errors.append("Invalid email or password")
            return render_template("auth/login.html", form=form)

        login_user(User(user), force=True)

        next = request.args.get("next")
        if not next:
            return redirect(url_for("templates.index"))
        return redirect(next)

    return render_template("auth/login.html", form=form)


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    db = get_db()
    if current_user.is_authenticated:
        return redirect(url_for("templates.index"))
    form = SignupForm()
    if form.validate_on_submit():
        data = form.data
        user = db.users.find_one({"email": data["email"]})
        if user is not None:
            form.form_errors.append("User already exists")
            return render_template("auth/signup.html", form=form)

        username = db.users.find_one({"username": data["username"]})
        if username is not None:
            form.form_errors.append("Username already taken")
            return render_template("auth/signup.html", form=form)

        hashed = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt())
        data["password"] = hashed.decode("utf-8")
        data["favorite_albums"] = []

        _id = db.users.insert_one(
            {
                "name": data["name"],
                "surname": data["surname"],
                "username": data["username"],
                "email": data["email"],
                "password": data["password"],
                "favorite_albums": data["favorite_albums"],
            }
        ).inserted_id

        login_user(User({"_id": _id, **data}), force=True)

        next = request.args.get("next")
        if not next:
            return redirect(url_for("templates.index"))
        return redirect(next)

    return render_template("auth/signup.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("templates.index"))
