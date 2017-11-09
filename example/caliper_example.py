import json

from flask import Flask, session, render_template, request

# Import related with Caliper
from caliper import events
from caliper.constants import BASIC_EVENT_ACTIONS

from context import *

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
        eventTime=datetime.datetime.now().isoformat(),
        membership=example_membership,
        session=example_session
    )

    navigation_event = events.NavigationEvent(
        actor=example_user,
        action=BASIC_EVENT_ACTIONS['NAVIGATED_TO'],
        object=homepage,
        eventTime=datetime.datetime.now().isoformat(),
        membership=example_membership,
        session=example_session
    )

    if 'user' not in session:
        # If you visit this page first, send SessionEvent
        session['user'] = 'caliper_test'
        sensor.send(session_event)
        event_type = getattr(session_event, 'type')
        action = getattr(session_event, 'action')
    else:
        # If you visited this page again, send NavigationEvent
        sensor.send(navigation_event)
        event_type = getattr(navigation_event, 'type')
        action = getattr(navigation_event, 'action')

    return render_template('index.html',
                           event=event_type,
                           action=action,
                           event_data=navigation_event.as_json(thin_context=True, thin_props=True))


@app.route('/read')
def reading_page():
    """
    Create and send NavigationEvent
    """
    navigation_event = events.NavigationEvent(
        actor=example_user,
        action=BASIC_EVENT_ACTIONS['NAVIGATED_TO'],
        object=reading_material,
        eventTime=datetime.datetime.now().isoformat(),
        membership=example_membership,
        session=example_session
    )

    event_type = getattr(navigation_event, 'type')
    action = getattr(navigation_event, 'action')

    sensor.send(navigation_event)

    return render_template('reading.html',
                           event=event_type,
                           action=action,
                           event_data=navigation_event.as_json(thin_context=True, thin_props=True))


@app.route('/tag', methods=['POST'])
def tag_page():
    """
    Generate tag and send AnnotationEvent
    """
    tags = list(tag for tag in request.form['tags'].split(','))

    # Tag
    generated_tag = entities.TagAnnotation(
        id=BASE_URI + "/user/193828/course/2017/ssed514/document/11/tag/1",
        annotator=example_user,
        annotated=reading_material,
        tags=tags
    )

    # Create and send AnnotationEvent
    annotation_event = events.AnnotationEvent(
        actor=example_user,
        action=BASIC_EVENT_ACTIONS['TAGGED'],
        object=reading_material,
        generated=generated_tag,
        eventTime=datetime.datetime.now().isoformat(),
        membership=example_membership,
        session=session
    )

    event_type = getattr(annotation_event, 'type')
    action = getattr(annotation_event, 'action')

    sensor.send(annotation_event)

    return render_template('reading.html',
                           event=event_type,
                           action=action,
                           event_data=annotation_event.as_json(thin_context=True, thin_props=True),
                           tags=tags)


@app.route('/quiz')
def quiz_page():
    """
    Create and send AssessmentEvent(Started)
    """
    assessment_event = events.AssessmentEvent(
        actor=example_user,
        action=BASIC_EVENT_ACTIONS['STARTED'],
        object=assessment,
        eventTime=datetime.datetime.now().isoformat(),
        membership=example_membership,
        session=session
    )

    event_type = getattr(assessment_event, 'type')
    action = getattr(assessment_event, 'action')

    sensor.send(assessment_event)

    return render_template('quiz.html',
                           event=event_type,
                           action=action,
                           event_data=assessment_event.as_json(thin_context=True, thin_props=True))


@app.route('/quiz_submit', methods=['POST'])
def quiz_submit():
    """
    Create and send AssessmentEvent(Submitted) and GradeEvent(Graded)
    """
    answer = int(request.form['test-question'])

    if answer == 2:
        score_given = 10.0
    else:
        score_given = 0.0

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
        scoreGiven=score_given,
        dateCreated=datetime.datetime.now().isoformat()
    )

    grade_event = events.GradeEvent(
        actor=ed_app,
        action=BASIC_EVENT_ACTIONS['GRADED'],
        object=attempt,
        generated=score,
        eventTime=datetime.datetime.now().isoformat(),
        membership=example_membership,
        session=example_session
    )

    # Test to send multiple events in list.
    sensor.send([assessment_event, grade_event])

    event_type = getattr(assessment_event, 'type') + " & " + getattr(grade_event, 'type')
    action = getattr(assessment_event, 'action') + " & " + getattr(grade_event, 'action')

    # To show AssessmentEvent & GradeEvent in JSON format.
    event_list = [
        assessment_event.as_dict(thin_context=True, thin_props=True),
        grade_event.as_dict(thin_props=True, thin_context=True)
    ]

    return render_template('quiz.html',
                           event=event_type,
                           action=action,
                           event_data=json.dumps(event_list),
                           answer=answer)
