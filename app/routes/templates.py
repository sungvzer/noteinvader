from json import dumps
from flask import Blueprint, render_template, request
from flask_login import login_required

from app.services.music import MusicService

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
    if has_query:
        res = MusicService.find_albums(query, page)
    else:
        res = None

    return render_template(
        "search.html",
        query=query,
        has_query=has_query,
        classname=f"{'has' if has_query else 'no'}-query",
        results=res,
    )
