"""
This is the flask app
"""
import json
from flask import Flask, render_template
from dotenv import load_dotenv
import requests
from app.utilities import md_to_html

load_dotenv()

app = Flask(__name__)

with open("./app/static/user-template.json", encoding="utf-8") as file:
    user = json.load(file)


@app.route("/")
def index():
    """
    Renders the homepage.
    """
    with open("./app/static/user-template.json", encoding="utf-8") as file:
        user = json.load(file)

    # ? I'm using some random persons API for preview reasons.
    projects = requests.get(f"https://ghapi.dstn.to/{user['github']}/pinned").json()
    user["about"] = md_to_html(user["about"])
    user["projects"] = projects["data"]

    return render_template("/pages/home.html", user=user)


@app.route("/project/<name>")
def project(name):
    """
    Renders a project page if available.
    """

    # ? We would actually look for the project page in a database.
    # ? For now let's serve this template
    file_path = "./app/static/project-template.md"

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    html = md_to_html(text)

    return render_template("/pages/project.html", user=user, content=html)


@app.errorhandler(404)
def page_not_found(_e):
    """
    Renders a 404 page whenever a user visits an unknown route.
    """
    return render_template("/pages/404.html"), 404
