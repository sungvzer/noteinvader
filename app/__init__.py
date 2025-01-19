from flask import Flask, render_template, send_from_directory
from flask.cli import load_dotenv
import os
from flask_pymongo import ObjectId, PyMongo
import flask_login

if not load_dotenv():
    print("Failed to load .env file")

mongo_settings = {
    "host": os.environ.get("MONGODB_HOST"),
    "port": os.environ.get("MONGODB_PORT"),
    "username": os.environ.get("MONGODB_USER"),
    "password": os.environ.get("MONGODB_PASS"),
    "database": os.environ.get("MONGODB_DATABASE"),
}


app = Flask(__name__)
app.config["MONGO_URI"] = (
    f"mongodb://{mongo_settings['username']}:{mongo_settings['password']}@{mongo_settings['host']}:{mongo_settings['port']}/{mongo_settings['database']}?authSource=admin"
)

app.secret_key = os.environ.get("SECRET_KEY")
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


mongo = PyMongo(
    app,
)


from app.models.user import User


@login_manager.user_loader
def load_user(user_id):
    """
    Dato un user_id, recupera l'utente da MongoDB.
    """
    assert mongo.db is not None, "MongoDB is not initialized"
    user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if user_data:
        return User(user_data)
    return None


def is_in_favorites(album_id, favorite_albums):
    return str(album_id) in [str(fav) for fav in favorite_albums]


def seconds_to_time_string(seconds: int | None):
    if seconds is None:
        return "0:00"
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    if hours > 0:
        return f"{hours}:{minutes:02}:{seconds:02}"
    return f"{minutes}:{seconds:02}"


# Register the filter
app.jinja_env.filters["is_in_favorites"] = is_in_favorites
app.jinja_env.filters["seconds_to_time_string"] = seconds_to_time_string

from app.routes.templates import templates
from app.routes.auth import auth
from app.routes.api.favorites import favorites

app.register_blueprint(templates)
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(favorites, url_prefix="/api/favorites")


# Support for old browsers
@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.errorhandler(404)
def page_not_found(_):
    return render_template("404.html"), 404


@app.context_processor
def inject_global_data():
    # Return data to be available globally in all templates
    return {"endpoints_with_no_navbar": []}
