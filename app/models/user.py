from flask_login import UserMixin
import json


class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data["_id"])  # Necessario per Flask-Login
        self.username = user_data["username"]
        self.password = user_data["password"]
        self.email = user_data["email"]
        self.name = user_data["name"]
        self.surname = user_data["surname"]
        self.favorite_albums = (
            user_data["favorite_albums"] if "favorite_albums" in user_data else []
        )
        self.following = user_data["following"] if "following" in user_data else []

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
