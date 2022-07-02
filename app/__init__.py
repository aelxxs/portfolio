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
from pylast import LastFMNetwork
import os

load_dotenv()

app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode.")
    db = SqliteDatabase("file:memory?mode=memory&cache=shared", uri=True)
else:
    db = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD") ,
        host=os.getenv("MYSQL_HOST"),

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


db.connect()
db.create_tables([TimelinePost])

fm = LastFMNetwork(api_key=getenv("LASTFM_API_KEY"), api_secret=getenv("LASTFM_SECRET"))


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


@app.route("/api/now_playing", methods=["GET"])
def now_playing():
    """
    Returns current song from lastfm.
    """
    alexis = fm.get_user("aelxxs")
    track = alexis.get_now_playing()

    song = None

    if track:
        song = {
            "url": track.get_url(),
            "name": track.get_name(),
            "artist": track.get_artist().get_name(),
            "cover": track.get_cover_image(),
        }

    return {"song": song}


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
    name = request.form.get('name', None)
    email = request.form.get('email', None)
    content = request.form.get('content', None)

    if not name or not len(name):
        return "Invalid name", 400

    if not email or not len(email) or "@" not in email:
        return "Invalid email", 400

    if not content or not len(content):
       return "Invalid content", 400

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
