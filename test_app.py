import os
import unittest
from datetime import date, timedelta

from app import create_app
from models import setup_db, Task, Sprint


class PrioritizerTestCase(unittest.TestCase):
    """This class represents the ___ test case"""

    def setUp(self):
        """Executed before each test. Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        # self.database_name = "postgres"
        # self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        # setup_db(self.app, self.database_path)

        # # binds the app to the current context
        # with self.app.app_context():
        #     self.db = SQLAlchemy()
        #     self.db.init_app(self.app)
        #     # create all tables
        #     self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_empty_test(self):
        """Test _____________ """
        # res = self.client().get('/')
        #
        # self.assertEqual(res.status_code, 200)
        pass

    def test_given_DB_should_CRUD_models(self):
        # create models
        sprint = Sprint(
            goal='create a capstone project',
            start_date=date.today(),
            end_date=date.today() + timedelta(15)
        )
        sprint.insert()
        self.assertIsNotNone(sprint.id)

        task = Task(
            description='finish the project',
            important=True,
            urgent=True,
            done=False,
            sprint_id=sprint.id
        )
        task.insert()
        self.assertIsNotNone(task.id)

        # delete objects
        sprint = Sprint.query.first()
        sprint.delete()

        task = Task.query.one_or_none()
        self.assertIsNone(task)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
