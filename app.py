from flask import Flask, json, Response
import os
app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}!</h1>'.format(name)

@app.route('/game/<num>')
def game(num):
    file_name = 'game' + num +'.json';
    full_path = os.path.join(app.root_path, 'game_boards', file_name);
    data = open(full_path)
    return Response(data, mimetype='application/json');

# app.add_url_rule('/user/<name>', 'user', user)


if __name__ == "__main__":
    app.run()
