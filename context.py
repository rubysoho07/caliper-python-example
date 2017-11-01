import datetime

import caliper
from caliper import entities

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
webpage = caliper.entities.WebPage(
    id=BASE_URI+"/course/2017/ssed514/document/11",
    name="Welfare Economics",
    description="Introduction of welfare economics"
)

# Sensor configuration
sensor_config = caliper.HttpOptions(
    host='https://requestb.in/test',
    auth_scheme='Bearer',
    api_key='test_api_key'
)

sensor = caliper.build_sensor_from_config(
    sensor_id='https://example.org/sensor',
    config_options=sensor_config
)
