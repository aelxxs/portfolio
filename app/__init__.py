"""
This is the flask app
"""
import json
from flask import Flask, render_template
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__)

with open("./app/static/user-template.json", encoding="utf-8") as file:
    user = json.load(file)


@app.route("/")
def index():
    """
    Renders the homepage.
    """

    # ? I'm using some random persons API for preview reasons.
    repos = requests.get(f"https://ghapi.dstn.to/{user['github']}/pinned").json()
    user["projects"] = repos["data"]

    return render_template("/pages/home.html", user=user, title=user["name"])


@app.route("/projects")
def projects():
    """
    Renders the projects page.
    """

    return render_template("/pages/projects.html", user=user, title="Projects")


@app.route("/thoughts")
def thoughts():
    """
    Renders the thoughts page.
    """

    return render_template("/pages/thoughts.html", user=user, title="Thoughts")


@app.errorhandler(404)
def page_not_found(_e):
    """
    Renders a 404 page whenever a user visits an unknown route.
    """
    return render_template("/pages/404.html", title="404"), 404
