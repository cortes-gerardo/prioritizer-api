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
the Stakeholder that can see and add as many tasks wants
the ScrumMaster that is in control of the sprint and can classify each task and delete them if needed.
and the Developers that can see all the tasks on the sprint.

## Contributing
### Code Style
Some guidelines to help with the code:
- Python code is using the [pep8](https://www.python.org/dev/peps/pep-0008/) style guide.
- For commits on Github [Udacity git commit message](https://udacity.github.io/git-styleguide/) style guide.

# Getting Started

## Prerequisites
- Python 3.7

## Local Development
Is recommended the use of virtual environment, in order to set it up, run the following commands:
```sh
# navigate to root project directory
$ cd /prioritizer-api

# create a virtual environment (venv) from a local python 3.7 installation
$ python3.7 -m venv venv

# activate the venv
$ . venv/bin/activate

# install the required libs in the venv 
(venv) $ pip install -r requirements.txt

# close the venv
(venv) $ deactivate
```

### Set up DB
In order to cleanly work with the DB, flask-migration is installed, please use the following commands to control the changes in the DB.
```sh
# create initial migration dir structure
(venv) $ python manage.py db init

# detects the changes and creates a migration file
(venv) $ python manage.py db migrate

# for upgrade the DB version
(venv) $ python manage.py db upgrade

# for downgrade the DB version
(venv) $ python manage.py db downgrade
```

## Local Tests
To run the test and ensure everything is working as it should, please run:
```sh
(venv) $ pytest
```

# API Reference *
WIP

# Deployment
WIP

# Authors
- [Gerardo Cortés](mailto:gerardo.cortes.o@gmail.com)

# Acknowledgements
