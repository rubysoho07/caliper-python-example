import datetime

from flask import Flask

# Import related with Caliper
from caliper import entities
from caliper.events import SessionEvent, NavigationEvent, AnnotationEvent, AssessmentEvent, GradeEvent
from caliper.constants import SESSION_EVENT_ACTIONS, NAVIGATION_EVENT_ACTIONS, ANNOTATION_EVENT_ACTIONS, \
    ASSESSMENT_EVENT_ACTIONS, GRADE_EVENT_ACTIONS

from context import BASE_URI, example_user, ed_app, sensor, webpage, tag, assessment

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
    # Create and send AnnotationEvent
    annotation_event = AnnotationEvent(
        actor=example_user,
        action=ANNOTATION_EVENT_ACTIONS['TAGGED'],
        object=webpage,
        generated=tag,
        eventTime=datetime.datetime.now().isoformat()
    )

    sensor.send(annotation_event)
    return 'Tagged'


@app.route('/quiz')
def quiz_page():
    # Create and send AssessmentEvent(Started)
    assessment_event = AssessmentEvent(
        actor=example_user,
        action=ASSESSMENT_EVENT_ACTIONS['STARTED'],
        object=assessment,
        eventTime=datetime.datetime.now().isoformat()
    )

    sensor.send(assessment_event)
    return 'Quiz Start!'


@app.route('/quiz_submit')
def quiz_submit():
    # Create and send AssessmentEvent(Submitted) and GradeEvent(Graded)
    assessment_event = AssessmentEvent(
        actor=example_user,
        action=ASSESSMENT_EVENT_ACTIONS['SUBMITTED'],
        object=assessment,
        eventTime=datetime.datetime.now().isoformat()
    )

    attempt = entities.Attempt(
        id=BASE_URI+"/course/2017/ssed514/assessment/1/attempt/1",
        assignee=example_user,
        assignable=assessment,
        count=1
    )

    score = entities.Score(
        id=BASE_URI + "/course/2017/ssed514/assessment/1/attempt/1",
        attempt=attempt,
        maxScore=15.0,
        scoreGiven=11.0,
        dateCreated=datetime.datetime.now().isoformat()
    )

    grade_event = GradeEvent(
        actor=ed_app,
        action=GRADE_EVENT_ACTIONS['GRADED'],
        object=attempt,
        generated=score,
        eventTime=datetime.datetime.now().isoformat()
    )

    sensor.send([assessment_event, grade_event])
    return 'Quiz submitted and graded!'
