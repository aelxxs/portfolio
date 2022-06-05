"""
This is the flask app
"""
from flask import Flask, render_template
from dotenv import load_dotenv
import requests
import markdown
import bleach

load_dotenv()

app = Flask(__name__)

# ! This is temp.
user = {
    "name": "John Doe",
    "icon": "https://umai.pw/2no_Vq",
    "github": "https://github.com",
    "linkedin": "https://linkedin.com",
    "email": "https://gmail.com",
    "resume": "https://www.google.com",
    "flags": [
        {"name": "US", "icon": "https://i.umai.pw/ZkGRdK.png"},
        {"name": "ES", "icon": "https://i.umai.pw/a6Jc-N.png"},
    ],
    "socials": [
        {
            "name": "Email",
            "icon": "https://i.umai.pw/drb5mM.svg",
            "link": "mailto:email@email.com",
        },
        {
            "name": "LinkedIn",
            "icon": "https://i.umai.pw/S8Fs_J.svg",
            "link": "https://linkedin.com",
        },
        {
            "name": "GitHub",
            "icon": "https://i.umai.pw/xhdarP.svg",
            "link": "https://github.com",
        },
        {
            "name": "Resume",
            "icon": "https://i.umai.pw/jLZRy7.svg",
            "link": "https://link-to-resume.com",
        },
    ],
}


@app.route("/")
def index():
    """
    This renders the homepage
    """
    projects = requests.get("https://ghapi.dstn.to/aelxxs/pinned").json()
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

    html = bleach.clean(
        markdown.markdown(text),
        tags=[
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "p",
            "em",
            "strong",
            "ul",
            "ol",
            "li",
            "code",
            "img",
        ],
        attributes={"img": ["src"]},
    )

    return render_template("/pages/project.html", user=user, content=html)


@app.errorhandler(404)
def page_not_found(_e):
    """
    Renders a 404 page whenever a user visits an unknown route.
    """
    return render_template("/pages/404.html"), 404
