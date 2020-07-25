# Prioritizer API
## Description
This project helps to prioritize assignments by using an abstraction of the [Eisenhower Matrix](https://en.wikipedia.org/wiki/Time_management#The_Eisenhower_Method). Each assignment is classified as _urgent_ or _important_ to encourage a course of action.

Assignments are grouped in Sprints were the Product Owner defines the _main goal_ and _duration_ of the sprint. Having the main goal present, gives contexts to classify something as important, and the duration is needed to know which assignments are becoming urgent.

- _Important_: likely to have a profound effect on success.
- _Urgent_: requiring immediate action or attention.

|               | Urgent            | Not Urgent  |
| ------------: | ----------------- |------------ |
| Important     | Do it             | Schedule it |
| Not Important | Delegate or Delay | Eliminate   |

There are 3 Actors:
the _Stakeholder_ that can see and add as many tasks wants,
the _ScrumMaster_ that is in control of the sprint and can classify each task and delete them if needed,
and the _Developer_ that can see all the tasks on the sprint.

## Contributing
- [How to Contribute](CONTRIBUTING.md)

# Getting Started
## Prerequisites
- Python 3.7

## Local Development
Is recommended the use of virtual environment, in order to set it up, run the following commands:
```sh
# navigate to root project directory
cd /prioritizer-api

# create a virtual environment (venv) from a local python 3.7 installation
python3.7 -m venv venv

# activate the (venv)
. venv/bin/activate

# install the required libs in the (venv)
pip install -r requirements.txt

# close the (venv)
deactivate
```

### Set up DB
In order to cleanly work with the DB, flask-migration is installed, please use the following commands to control the changes in the DB.
```sh
# while inside the (venv)
# create initial migration dir structure
python manage.py db init

# detects the changes and creates a migration file
python manage.py db migrate

# for upgrade the DB version
python manage.py db upgrade

# for downgrade the DB version
python manage.py db downgrade
```

## Local Tests
To run the test and ensure everything is working as it should, please run:
```sh
pytest
```

# API Documentation
- [API documentation](API_DOCUMENTATION.md)

# Deployment
WIP

# Authors
- [Gerardo Cortés](mailto:gerardo.cortes.o@gmail.com)

# Acknowledgements
