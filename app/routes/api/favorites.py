from flask import Blueprint
from flask_login import login_required, current_user
from flask_pymongo import ObjectId

from app import is_in_favorites
from app.utils.db import get_db

favorites = Blueprint("api_favorites", __name__)


@favorites.route("/<album_id>", methods=["POST"])
@login_required
def toggle_favorites(album_id):
    user = current_user
    album_id = ObjectId(album_id)
    if is_in_favorites(album_id, user.favorite_albums):
        user.favorite_albums.remove(album_id)
    else:
        user.favorite_albums.append(album_id)
    db = get_db()
    db.users.update_one(
        {"_id": ObjectId(user.id)},
        {"$set": {"favorite_albums": user.favorite_albums}},
    )

    db.music.update_one(
        {"_id": album_id},
        {
            "$inc": {
                "stars": (1 if is_in_favorites(album_id, user.favorite_albums) else -1)
            }
        },
    )
    return "", 204
