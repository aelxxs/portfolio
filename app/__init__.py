"""
This is the flask app
"""
import datetime
from os import getenv
from dotenv import load_dotenv
from requests import get
from peewee import *
from flask import Flask, render_template, request
from playhouse.shortcuts import model_to_dict

load_dotenv()

app = Flask(__name__)


db = MySQLDatabase(
    getenv("MYSQL_DATABASE"),
    host=getenv("MYSQL_HOST"),
    user=getenv("MYSQL_USER"),
    password=getenv("MYSQL_PASSWORD"),
)


class TimelinePost(Model):
    """
    Represents a timeline post
    """

    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        """
        Model metadata
        """

        database = db


# db.connect()
# db.create_tables([TimelinePost])


@app.route("/")
def index():
    """
    Renders the homepage.
    """

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


@app.route("/timeline")
def timeline():
    """
    Renders the timeline page.
    """

    posts = TimelinePost.select().order_by(TimelinePost.created_at.desc())

    return render_template("/pages/timeline.html", title="Timeline", timeline=posts)


@app.errorhandler(404)
def page_not_found(_e):
    """
    Renders a 404 page whenever a user visits an unknown route.
    """
    return render_template("/pages/404.html", title="404"), 404


#
# API ENDPOINTS – WILL NOT BE MAINTAINED
#


@app.route("/api/timeline_post", methods=["GET"])
def get_timeline():
    """
    Retrieves all timeline posts in descending order.
    """

    posts = TimelinePost.select().order_by(TimelinePost.created_at.desc())
    timeline = [model_to_dict(post) for post in posts]

    return {"timeline": timeline}


@app.route("/api/timeline_post", methods=["POST"])
def add_timeline():
    """
    Adds a new post to the timeline.
    """

    name = request.form["name"]
    email = request.form["email"]
    content = request.form["content"]

    post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(post)


@app.route("/api/timeline_post", methods=["DELETE"])
def del_timeline():
    """
    Delete a post from the timeline.
    """

    post_id = request.form["id"]

    TimelinePost.delete_by_id(post_id)

    return "deleted post"
