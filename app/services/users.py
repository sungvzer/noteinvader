from bson.json_util import dumps
from flask.typing import ResponseValue
from werkzeug.wrappers import response
from app.models.user import User
from app.utils.db import get_db


class UsersService:
    __instance = None

    @staticmethod
    def get():
        if UsersService.__instance is None:
            UsersService()
        return UsersService.__instance

    def __init__(self):
        if UsersService.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            UsersService.__instance = self

    def create_user(self, user: User) -> ResponseValue:
        db = get_db()

        existing_user = db.users.find_one({"email": user.email})

        if existing_user is not None:
            return response.Response(
                status=400,
                mimetype="application/json",
                response=dumps({"error": "User already exists"}),
            )

        inserted_user_id = db.users.insert_one(user).inserted_id
        inserted_user = db.users.find_one({"_id": inserted_user_id})

        return response.Response(
            status=201, mimetype="application/json", response=dumps(inserted_user)
        )
