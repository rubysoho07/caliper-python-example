import datetime, uuid

from flask import Flask
from context import *

# Import related with Caliper
from caliper import events
from caliper.constants import SESSION_EVENT_ACTIONS

app = Flask(__name__)


@app.route('/')
def first_page():
    # TODO: Make SessionEvent if a session doesn't exist, or make NavigationEvent.
    try:
        session_event = events.SessionEvent(
            id='urn:uuid:{}'.format(uuid.uuid4()),
            actor=example_user,
            action=SESSION_EVENT_ACTIONS['LOGGED_IN'],
            object=ed_app,
            eventTime=str(datetime.datetime.now().isoformat())
        )

        sensor.send(session_event)
    except Exception as e:
        print(e)
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
