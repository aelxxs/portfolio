from flask import Flask, render_template

app = Flask(__name__)

# ! This is temp.
user = {
    "name": "John Doe",
    "icon": "https://umai.pw/2no_Vq"
}

@app.route('/')
def index():
    return render_template('/pages/home.html', user=user)
