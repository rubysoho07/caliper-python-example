import datetime

import caliper
from caliper import entities
from caliper.constants import CALIPER_ROLES, CALIPER_STATUS

BASE_URI = "http://example.org"

# User
example_user = caliper.entities.Person(
    id=BASE_URI+"/user/193828",
    dateCreated=datetime.datetime(year=2017, month=10, day=20, hour=14, minute=9, second=43).isoformat(),
    name="Test User"
)

# Course
example_course = caliper.entities.CourseSection(
    id=BASE_URI+"/course/2017/ssed514",
    courseNumber="SSED514",
    name="Economy and Society",
    category="lecture",
    dateCreated=datetime.date(year=2017, month=8, day=24).isoformat()
)

# SoftwareApplication
ed_app = caliper.entities.SoftwareApplication(
    id=BASE_URI+"/sampleCaliperApp",
    name="Sample Caliper Application",
    dateCreated=datetime.date(year=2017, month=7, day=11).isoformat()
)

# Page
homepage = caliper.entities.DigitalResource(
    id=BASE_URI + "/course/2017/ssed514/",
    name="Lecture Introduction",
    description="Lecture Introduction"
)

reading_material = caliper.entities.WebPage(
    id=BASE_URI+"/course/2017/ssed514/document/11",
    name="Welfare Economics",
    description="Introduction of welfare economics"
)

# Assessment
assessment = caliper.entities.Assessment(
    id=BASE_URI+"/course/2017/ssed514/assessment/1",
    name="Questions for Economics",
    isPartOf=example_course,
    dateCreated=datetime.date(year=2017, month=8, day=12).isoformat(),
    dateModified=datetime.date(year=2017, month=8, day=19).isoformat(),
    maxAttempts=3,
    maxSubmits=2,
    maxScore=15.0
)

# Membership
example_membership = caliper.entities.Membership(
    id=BASE_URI+"/course/2017/ssed514" + "/member/193828",
    member=example_user,
    organization=example_course,
    roles=[CALIPER_ROLES['LEARNER']],
    status=CALIPER_STATUS['ACTIVE'],
    dateCreated=datetime.date(year=2015, month=3, day=11).isoformat()
)

# Session
example_session = caliper.entities.Session(
    id=BASE_URI+"/session/348904137905317",
    user=example_user,
    startedAtTime=datetime.datetime.now()
)

# Sensor configuration
sensor_config = caliper.HttpOptions(
    host='https://requestb.in/r5f8qdr5',
    auth_scheme='Bearer',
    api_key='test_api_key'
)

sensor = caliper.build_sensor_from_config(
    sensor_id='https://example.org/sensor',
    config_options=sensor_config
)
