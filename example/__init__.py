from flask import Flask

app = Flask(__name__)


@app.route('/')
def first_page():
    # TODO: Make SessionEvent if a session doesn't exist, or make NavigationEvent.
    return 'Test page!'


@app.route('/read')
def reading_page():
    # TODO: Make NavigationEvent
    return 'Reading material!'


@app.route('/tag')
def tag_page():
    # TODO: Make AnnotationEvent
    return 'Tagged'


@app.route('/quiz')
def quiz_page():
    # TODO: Make AssessmentEvent
    return 'Quiz Start!'


@app.route('/quiz_submit')
def quiz_submit():
    # TODO: Make GradeEvent
    return 'Quiz submitted and graded!'
