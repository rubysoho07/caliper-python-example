import datetime

from flask import Flask

# Import related with Caliper
from caliper.events import SessionEvent, NavigationEvent
from caliper.constants import SESSION_EVENT_ACTIONS, NAVIGATION_EVENT_ACTIONS

from context import example_user, ed_app, sensor, webpage

app = Flask(__name__)


@app.route('/')
def first_page():
    # TODO: Make SessionEvent if a session doesn't exist, or make NavigationEvent.
    session_event = SessionEvent(
        actor=example_user,
        action=SESSION_EVENT_ACTIONS['LOGGED_IN'],
        object=ed_app,
        eventTime=datetime.datetime.now().isoformat()
    )

    sensor.send(session_event)
    return 'Test page!'


@app.route('/read')
def reading_page():
    # Create and send NavigationEvent
    navigation_event = NavigationEvent(
        actor=example_user,
        action=NAVIGATION_EVENT_ACTIONS['NAVIGATED_TO'],
        object=webpage,
        eventTime=datetime.datetime.now().isoformat()
    )

    sensor.send(navigation_event)
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
