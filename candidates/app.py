from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)


@app.route("/")
def home():
    return "Application Tracking System"


'''
CORS(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run()
'''