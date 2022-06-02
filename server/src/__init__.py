from flask import Flask

# I think this works?
app = Flask(__name__, static_folder='../../client/dist', static_url_path='/')

@app.route('/')
def index():
    return app.send_static_file('index.html')