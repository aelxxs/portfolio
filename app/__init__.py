"""
This is the flask app
"""
from flask import Flask, render_template
from dotenv import load_dotenv
from requests import get

load_dotenv()

app = Flask(__name__)


@app.route("/")
def index():
    """
    Renders the homepage.
    """

    # ? I'm using some random persons API for preview reasons.
    repos = get("https://ghapi.dstn.to/aelxxs/pinned").json()["data"]

    return render_template("/pages/home.html", title="Alexis Vielma", repos=repos)


@app.route("/projects")
def projects():
    """
    Renders the projects page.
    """

    return render_template("/pages/projects.html", title="Projects")


@app.route("/thoughts")
def thoughts():
    """
    Renders the thoughts page.
    """

    return render_template("/pages/thoughts.html", title="Thoughts")


@app.errorhandler(404)
def page_not_found(_e):
    """
    Renders a 404 page whenever a user visits an unknown route.
    """
    return render_template("/pages/404.html", title="404"), 404
