from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from flask_pymongo import ObjectId

from app.utils.db import get_db

users = Blueprint("api_users", __name__)


@users.route("/follow", methods=["POST"])
@login_required
def toggle_follow():
    user = current_user
    json = request.json
    if json is None:
        return "Invalid request", 400
    username = json.get("username")
    if username is None:
        return "Invalid request", 400

    if username in user.following:
        user.following.remove(username)
    else:
        user.following.append(username)

    db = get_db()
    db.users.update_one(
        {"_id": ObjectId(user.id)},
        {"$set": {"following": user.following}},
    )
    return jsonify({"isFollowing": username in user.following}), 200
