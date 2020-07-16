import json
import os
import unittest
from flask_sqlalchemy import SQLAlchemy
from datetime import date, timedelta
from sqlalchemy import create_engine

from app import create_app
from models import setup_db, Task, Sprint


class PrioritizerTestCase(unittest.TestCase):
    """This class represents the ___ test case"""

    def setUp(self):
        """Executed before each test. Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        # self.database_name = "postgres"
        self.database_path = "postgres://postgres:password!@localhost:5432/postgres"  # .format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        sprint = Sprint(
            goal='mock sprint',
            start_date=date.today(),
            end_date=date.today() + timedelta(15)
        )
        sprint.insert()
        self.mock_sprint_id = sprint.id

        task = Task(
            description='mock task',
            important=True,
            urgent=True,
            done=False,
            sprint_id=sprint.id
        )
        task.insert()
        self.mock_task_id = task.id

    def tearDown(self):
        tasks = Task.query.all()
        for task in tasks:
            task.delete()

        sprints = Sprint.query.all()
        for sprint in sprints:
            sprint.delete()

    def test_when_get_sprints_then_200(self):
        res = self.client().get('/sprints')
        data = json.loads(res.data)

        self.assertEqual(200, res.status_code)
        self.assertEqual(True, data['success'])

    def test_when_post_sprints_then_201(self):
        res = self.client().post('/sprints',
                                 json={
                                     'goal': 'try to take over the world!',
                                     'start_date': '2020-08-12',
                                     'end_date': '2020-08-19'
                                 })
        data = json.loads(res.data)

        self.assertEqual(201, res.status_code)
        self.assertEqual(True, data['success'])

    def test_when_post_sprints_then_400(self):
        res = self.client().post('/sprints', json={})
        data = json.loads(res.data)

        self.assertEqual(400, res.status_code)
        self.assertEqual(False, data['success'])

    def test_when_post_sprints_then_422(self):
        res = self.client().post('/sprints',
                                 json={
                                     'goal': 'mock sprint',
                                     'start_date': '2020-08-12',
                                     'end_date': '2020-08-19'
                                 })
        data = json.loads(res.data)

        self.assertEqual(422, res.status_code)
        self.assertEqual(False, data['success'])

    def test_when_patch_sprints_then_200(self):
        res = self.client().patch('/sprints/%d' % self.mock_sprint_id,
                                  json={
                                      'goal': 'try to take over the world!'
                                  })
        data = json.loads(res.data)

        self.assertEqual(200, res.status_code)
        self.assertEqual(True, data['success'])

    def test_when_patch_sprints_then_400(self):
        res = self.client().patch('/sprints/%d' % self.mock_sprint_id,
                                  json={})
        data = json.loads(res.data)

        self.assertEqual(400, res.status_code)
        self.assertEqual(False, data['success'])
        # null payload
        # invalid dates format

    def test_when_patch_sprints_then_404(self):
        res = self.client().patch('/sprints/0', json={})
        data = json.loads(res.data)

        self.assertEqual(404, res.status_code)
        self.assertEqual(False, data['success'])

    def test_when_patch_sprints_then_422(self):
        # unique constrain broken
        existing_sprint = Sprint(
            goal='duplicate goal',
            start_date=date.today(),
            end_date=date.today()
        )
        existing_sprint.insert()

        res = self.client().patch(
            '/sprints/%d' % self.mock_sprint_id,
            json={
                'goal': 'duplicate goal'
            }
        )
        data = json.loads(res.data)

        self.assertEqual(422, res.status_code)
        self.assertEqual(False, data['success'])
        existing_sprint.delete()

    def test_when_delete_sprints_then_200(self):
        res = self.client().delete('/sprints/%d' % self.mock_sprint_id)
        data = json.loads(res.data)

        self.assertEqual(200, res.status_code)
        self.assertEqual(True, data['success'])

    def test_when_delete_sprints_then_404(self):
        res = self.client().delete('/sprints/0')
        data = json.loads(res.data)

        self.assertEqual(404, res.status_code)
        self.assertEqual(False, data['success'])

    def test_when_get_tasks_then_200(self):
        res = self.client().get('/sprints/%d/tasks' % self.mock_sprint_id)
        data = json.loads(res.data)

        self.assertEqual(200, res.status_code)
        self.assertEqual(True, data['success'])

    def test_when_get_tasks_then_404(self):
        res = self.client().get('/sprints/0/tasks')
        data = json.loads(res.data)

        self.assertEqual(404, res.status_code)
        self.assertEqual(False, data['success'])

    def test_when_post_tasks_then_201(self):
        res = self.client().post('/sprints/%d/tasks' % self.mock_sprint_id,
                                 json={
                                     'description': 'buys every property in the world above its 39th floor',
                                     'important': True,
                                     'urgent': True,
                                     'done': False
                                 })
        data = json.loads(res.data)

        self.assertEqual(201, res.status_code)
        self.assertEqual(True, data['success'])

    def test_when_post_tasks_then_400(self):
        # all null values
        res = self.client().post('/sprints/%d/tasks' % self.mock_sprint_id,
                                 json={})
        data = json.loads(res.data)

        self.assertEqual(400, res.status_code)
        self.assertEqual(False, data['success'])

    def test_when_post_tasks_then_404(self):
        # not found
        res = self.client().post('/sprints/0/tasks',
                                 json={
                                     'description': 'buys every property in the world above its 39th floor',
                                     'important': True,
                                     'urgent': True,
                                     'done': False
                                 })
        data = json.loads(res.data)

        self.assertEqual(404, res.status_code)
        self.assertEqual(False, data['success'])

    def test_when_patch_tasks_then_200(self):
        res = self.client().patch('/tasks/%d' % self.mock_task_id,
                                  json={
                                      'done': True
                                  })
        data = json.loads(res.data)

        self.assertEqual(200, res.status_code)
        self.assertEqual(True, data['success'])

    def test_when_patch_tasks_then_400(self):
        # all null values
        res = self.client().patch('/tasks/%d' % self.mock_task_id,
                                  json={
                                  })
        data = json.loads(res.data)

        self.assertEqual(400, res.status_code)
        self.assertEqual(False, data['success'])

    def test_when_patch_tasks_then_404(self):
        # not found
        res = self.client().patch('/tasks/0',
                                  json={
                                      'done': True
                                  })
        data = json.loads(res.data)

        self.assertEqual(404, res.status_code)
        self.assertEqual(False, data['success'])

    def test_when_delete_tasks_then_200(self):
        res = self.client().delete('/tasks/%d' % self.mock_task_id)
        data = json.loads(res.data)

        self.assertEqual(200, res.status_code)
        self.assertEqual(True, data['success'])

    def test_when_delete_tasks_then_404(self):
        # does not exist?
        res = self.client().delete('/tasks/0')
        data = json.loads(res.data)

        self.assertEqual(404, res.status_code)
        self.assertEqual(False, data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
