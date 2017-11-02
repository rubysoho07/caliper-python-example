import datetime

from flask import Flask, session, render_template

# Import related with Caliper
from caliper import entities, events
from caliper.constants import BASIC_EVENT_ACTIONS

from context import BASE_URI, example_user, ed_app, sensor, homepage, reading_material, tag, assessment

app = Flask(__name__)
app.secret_key = "XdZtfSQudavnsZeg9Bp7R2GwuKRtCUe9"


@app.route('/')
def first_page():
    """
    Create and send SessionEvent if a session doesn't exist,
    or create and send NavigationEvent.
    """
    session_event = events.SessionEvent(
        actor=example_user,
        action=BASIC_EVENT_ACTIONS['LOGGED_IN'],
        object=ed_app,
        eventTime=datetime.datetime.now().isoformat()
    )

    navigation_event = events.NavigationEvent(
        actor=example_user,
        action=BASIC_EVENT_ACTIONS['NAVIGATED_TO'],
        object=homepage,
        eventTime=datetime.datetime.now().isoformat()
    )

    if 'user' not in session:
        session['user'] = 'caliper_test'
        sensor.send(session_event)
        event_type = getattr(session_event, 'type')
        action = getattr(session_event, 'action')
    else:
        sensor.send(navigation_event)
        event_type = getattr(navigation_event, 'type')
        action = getattr(navigation_event, 'action')

    return render_template('index.html',
                           event=event_type,
                           action=action,
                           event_data=navigation_event.as_json(thin_props=True))


@app.route('/read')
def reading_page():
    # Create and send NavigationEvent
    navigation_event = events.NavigationEvent(
        actor=example_user,
        action=BASIC_EVENT_ACTIONS['NAVIGATED_TO'],
        object=reading_material,
        eventTime=datetime.datetime.now().isoformat()
    )

    event_type = getattr(navigation_event, 'type')
    action = getattr(navigation_event, 'action')

    sensor.send(navigation_event)
    return render_template('reading.html',
                           event=event_type,
                           action=action,
                           event_data=navigation_event.as_json(thin_props=True))


@app.route('/tag')
def tag_page():
    # Create and send AnnotationEvent
    annotation_event = events.AnnotationEvent(
        actor=example_user,
        action=BASIC_EVENT_ACTIONS['TAGGED'],
        object=reading_material,
        generated=tag,
        eventTime=datetime.datetime.now().isoformat()
    )

    sensor.send(annotation_event)
    return 'Tagged'


@app.route('/quiz')
def quiz_page():
    # Create and send AssessmentEvent(Started)
    assessment_event = events.AssessmentEvent(
        actor=example_user,
        action=BASIC_EVENT_ACTIONS['STARTED'],
        object=assessment,
        eventTime=datetime.datetime.now().isoformat()
    )

    event_type = getattr(assessment_event, 'type')
    action = getattr(assessment_event, 'action')

    sensor.send(assessment_event)
    return render_template('quiz.html',
                           event=event_type,
                           action=action,
                           event_data=assessment_event.as_json(thin_props=True))


@app.route('/quiz_submit')
def quiz_submit():
    # Create and send AssessmentEvent(Submitted) and GradeEvent(Graded)
    assessment_event = events.AssessmentEvent(
        actor=example_user,
        action=BASIC_EVENT_ACTIONS['SUBMITTED'],
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

    grade_event = events.GradeEvent(
        actor=ed_app,
        action=BASIC_EVENT_ACTIONS['GRADED'],
        object=attempt,
        generated=score,
        eventTime=datetime.datetime.now().isoformat()
    )

    sensor.send([assessment_event, grade_event])
    return 'Quiz submitted and graded!'
