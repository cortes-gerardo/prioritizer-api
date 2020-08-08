# Prioritizer API
## Description
This project helps to prioritize assignments by using an abstraction of the [Eisenhower Matrix](https://en.wikipedia.org/wiki/Time_management#The_Eisenhower_Method). Each assignment is classified as _urgent_ or _important_ to encourage a course of action.

Assignments are grouped in Sprints were the Product Owner defines the _main goal_ and _duration_ of the sprint. Having the main goal present gives contexts to classify something as important, and the duration is needed to know which assignments are becoming urgent.

- _Important_: likely to have a profound effect on success.
- _Urgent_: requiring immediate action or attention.

|               | Urgent            | Not Urgent   |
| ------------: | ----------------- | ------------ |
| Important     | Do it             | Schedule it  |
| Not Important | Delegate or Delay | Eliminate it |

A simple interface is provided to help with the visualization of data and the generation of the `JWT`. 

![prioritizer-api](screenshot-prioritizer-api.png)

There are 3 Actors:

The _Stakeholder_ that can see and add as many tasks want,
the _ScrumMaster_ that is in control of the sprint and can classify each task and delete them if needed,
and the _Public User_ (or the Developer) that can see all the tasks on the sprint.

For testing purposes, dummy accounts for the _Stakeholder_ and _ScrumMaster_ with permissions are already provided.

> User: scrummaster@cortes-gerardo.com
> Pass: 123Queso.

> User: stakeholder@cortes-gerardo.com
> Pass: 123Queso.

## Contributing
- [How to Contribute](CONTRIBUTING.md)

# Getting Started
## Prerequisites
- Python 3.7

## Local Development
Is recommended the use of a virtual environment, in order to set it up, run the following commands:
```sh
# navigate to the root project directory
cd /prioritizer-api

# create a virtual environment (venv) from a local python 3.7 installation
python3.7 -m venv venv

# activate the (venv)
. venv/bin/activate

# install the required libs in the (venv)
pip install -r requirements.txt

# to close the (venv)
deactivate
```
Once the dependencies are installed, the DB needs to be set up as follows. 

### Set up DB
In order to cleanly work with the DB, a `PostgreSQL`'s `Docker` image is used with `flask-migration`. Please use the following commands to control the changes in the DB.
```sh
# while runing the (venv)

# pull the docker image
docker pull postgres:latest

# run the postgres DB image
docker run --name psql -e POSTGRES_DB=prioritizer -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:latest

# set environment variable to connect with the DB
export DATABASE_URL=postgres://postgres:password@localhost:5432/prioritizer

# set up the DB tables
python manage.py db upgrade
```

## Local Tests
To run the test and ensure everything is working as it should, please use a clean DB version:
```sh
# while runing the (venv)

# run the test DB
docker run --name psql_test -e POSTGRES_DB=prioritizer_test -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:latest

# set environment variable
export DATABASE_URL=postgres://postgres:password@localhost:5432/prioritizer_test

# run the tests
pytest

# stop the test DB
docker stop psql_test

# remove container to use a new DB
docker container rm psql_test
```

The tests will run using a _ScrumMaster_ token, to tests the behavior of different accounts a postman file is included `Prioritizer.postman_collection.json`

To run the Postman tests are recommended to use a clean DB copy because it will use IDs of value 1 for both sprint and task; both set as variables in postman.  

# API Documentation
- [API documentation](API.md)

# Deployment
The project is stored in [GitHub](https://github.com/cortes-gerardo/prioritizer-api) each merge to the master branch is deployed to [Heroku](https://prioritizer-api.herokuapp.com/)

# Authors
- [Gerardo Cortés](mailto:gerardo.cortes.o@gmail.com)
