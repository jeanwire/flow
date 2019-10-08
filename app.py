from flask import Flask, json, Response, redirect
from flask_cors import CORS
import os
import random
import json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# allows redirects
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:G8AR7Cseu5bTh9pPttcX@localhost/flowgames'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# databse model
class Flow_Games(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    game_board = db.Column(db.JSON)

    def __repr__(self):
        return f'<Board: {self.id} {self.game_board}>'

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

@app.route('/users/<name>')
def user(name):
    return '<h1>Hello, {}!</h1>'.format(name)

@app.route('/play')
def choose_game():
    game_num = random.randint(1, 5)
    return redirect(f'/game/{game_num}')

@app.route('/game/<num>')
def game(num):
    game = json.dumps(Flow_Games.query.filter_by(id=num).first().game_board)

    return Response(game, mimetype='application/json')


if __name__ == "__main__":
    app.run()
