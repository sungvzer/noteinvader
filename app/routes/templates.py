from flask import Blueprint, render_template, request
from flask_login import login_required

templates = Blueprint("templates", __name__)


@templates.route("/")
def index():
    return render_template("index.html")


@templates.route("/search")
@login_required
def search():
    query = request.args.get("q")
    has_query = bool(query)
    return render_template(
        "search.html",
        query=query,
        has_query=has_query,
        classname=f"{'has' if has_query else 'no'}-query",
    )
