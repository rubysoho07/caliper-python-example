from flask import Flask

app = Flask(__name__)


@app.route('/')
def first_page():
    return 'Test page!'


@app.route('/read')
def reading_page():
    return 'Reading material!'


@app.route('/quiz')
def quiz_page():
    return 'Quiz Start!'
