from flask import Flask, json, Response, redirect
from flask_cors import CORS
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# allows redirects
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:G8AR7Cseu5bTh9pPttcX@localhost/dvdrental'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

@app.route('/users/<name>')
def user(name):
    return '<h1>Hello, {}!</h1>'.format(name)

@app.route('/play')
def choose_game():
    return redirect('/game/1')

@app.route('/game/<num>')
def game(num):
    file_name = 'game' + num +'.json';
    full_path = os.path.join(app.root_path, 'game_boards', file_name);
    data = open(full_path)
    return Response(data, mimetype='application/json');


if __name__ == "__main__":
    app.run()
