from flask import Blueprint, render_template, request, url_for
from flask_login import current_user, login_required
from flask_pymongo import ObjectId

from app.models.user import User
from app.services.music import MusicService
from app.utils.db import get_db

templates = Blueprint("templates", __name__)


@templates.route("/")
def index():
    return render_template("index.html")


@templates.route("/search")
@login_required
def search():
    query = request.args.get("q")
    page = request.args.get("page", 1)
    page = int(page)
    if page < 1:
        page = 1
    has_query = bool(query)

    pages = None
    res = None
    if has_query:
        res = MusicService.find_albums(query, page)
        total_results = int(res["totalResults"]) if "totalResults" in res else 0
        items_per_page = int(res["itemsPerPage"]) if "itemsPerPage" in res else 0
        pages = total_results // items_per_page + 1 if items_per_page > 0 else 0

    return render_template(
        "search.html",
        query=query,
        has_query=has_query,
        classname=f"{'has' if has_query else 'no'}-query",
        results=res,
        pages=pages,
        page=page,
        len=len,
    )


@templates.route("/album/<album_id>")
@login_required
def album(album_id: str):
    album = MusicService.get_album(ObjectId(album_id))
    users_with_album = MusicService.find_following_with_album(
        ObjectId(album_id), limit=4
    )

    get_username_span = (
        lambda user: f'<a href={url_for("templates.user", username=user["username"])} class="also_likes">{user["username"]}</a>'
    )

    if users_with_album is not None and len(users_with_album) == 0:
        users_with_album = None
    elif len(users_with_album) == 1:
        users_with_album = (
            f"{get_username_span(users_with_album[0])} also likes this album!"
        )
    elif len(users_with_album) == 2:
        users_with_album = f"{get_username_span(users_with_album[0])} and {get_username_span(users_with_album[1])} also like this album!"
    elif len(users_with_album) > 2:
        users_with_album = f"{', '.join([get_username_span(user) for user in users_with_album[:-1]])}, and {get_username_span(users_with_album[-1])} also like this album!"

    return render_template("album.html", album=album, users_with_album=users_with_album)


@templates.route("/user/<username>")
@login_required
def user(username: str):
    is_current_user = current_user.username == username

    user: User | None = None
    is_following = False
    followers = get_db().users.count_documents({"following": username})
    if is_current_user:
        user = User({**current_user.__dict__, "_id": ObjectId(current_user.id)})
    else:
        found = get_db().users.find_one({"username": username})
        if found is None:
            return render_template("404.html"), 404
        user = User(found)
        is_following = user.username in current_user.following

    favorite_albums = MusicService.get_albums(user.favorite_albums)

    return render_template(
        "user.html",
        user=user,
        is_current_user=is_current_user,
        is_following=is_following,
        len=len,
        followers=followers,
        favorite_albums=favorite_albums,
    )
