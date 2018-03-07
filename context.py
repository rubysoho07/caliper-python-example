import datetime

import caliper
from caliper import entities
from caliper.constants import CALIPER_ROLES, CALIPER_STATUS

BASE_URI = "http://example.org"
COURSE_IRI = BASE_URI+"/course/2017/ssed514"

# User
example_user = entities.Person(
    id=BASE_URI+"/user/193828",
    name="Test User"
)

# Course
example_course = entities.CourseSection(
    id=COURSE_IRI,
    courseNumber="SSED514",
    name="Economy and Society",
    category="lecture",
)

# SoftwareApplication
ed_app = entities.SoftwareApplication(
    id=BASE_URI+"/sampleCaliperApp",
    name="Sample Caliper Application",
)

# Page
homepage = entities.DigitalResource(
    id=COURSE_IRI,
    name="Lecture Introduction",
    description="Lecture Introduction"
)

reading_material = entities.WebPage(
    id=COURSE_IRI+"/document/11",
    name="Welfare Economics",
    description="Introduction of welfare economics"
)

# Assessment
assessment = entities.Assessment(
    id=COURSE_IRI+"/assessment/1",
    name="Questions for Economics",
    isPartOf=example_course,
    maxAttempts=3,
    maxSubmits=2,
    maxScore=15.0
)

# Membership
example_membership = entities.Membership(
    id=COURSE_IRI+"/member/193828",
    member=example_user,
    organization=example_course,
    roles=[CALIPER_ROLES['LEARNER']],
    status=CALIPER_STATUS['ACTIVE'],
)

# Session
example_session = entities.Session(
    id=BASE_URI+"/session/348904137905317",
    user=example_user,
)

# Sensor configuration
sensor_config = caliper.HttpOptions(
    host='https://caliper.imsglobal.org/caliper/849fab7f-72a4-4398-a4e5-e0eaec97170b/message',
    auth_scheme='Bearer',
    api_key='849fab7f-72a4-4398-a4e5-e0eaec97170b'
)

sensor = caliper.build_sensor_from_config(
    sensor_id='https://example.org/sensor',
    config_options=sensor_config
)
