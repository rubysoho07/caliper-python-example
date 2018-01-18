# Caliper Python Example

## Requirements

* Python 3.x (This example may not work well on Python 2.x)

## Install

* Install Caliper 1.1 (From source)

```
$ git clone https://github.com/IMSGlobal/caliper-python-public.git
$ pip install -e caliper-python-public
```

* Install prerequisites

```
$ pip install -r requirements.txt
```

* Edit endpoint configuration (`context.py`)

```python
# Sensor configuration
import caliper

sensor_config = caliper.HttpOptions(
    host='https://requestb.in/12345678',    # Endpoint address
    auth_scheme='Bearer',
    api_key='test_api_key'
)
```

* Run test server (Default port number is 5000 for Flask application.)

```
$ python main.py
```

## How To Use

Type `http://localhost:5000` on your web browser.

* Home `http://localhost:5000`

If you connect to this sample program, SessionEvent will be created and sent.

* Reading `http://localhost:5000/read`

If you move to this page, NavigationEvent will be created and sent. And you can make tags for this reading material. If you create tags, AnnotationEvent will be created and sent. 

* Quiz `http://localhost:5000/quiz`

If you move to this page, AssessmentEvent will be created and sent. And you submit an answer for this quiz, AssessmentEvent and GradeEvent will be created and sent.