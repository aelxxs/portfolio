"""
This is the flask app
"""
from flask import Flask, render_template
from dotenv import load_dotenv

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
}


@app.route("/")
def index():
    """
    This renders the homepage
    """
    return render_template("/pages/home.html", user=user)


@app.errorhandler(404)
def page_not_found(_e):
    """
    Renders a 404 page whenever a user visits an unknown route.
    """
    return render_template("/pages/404.html"), 404
