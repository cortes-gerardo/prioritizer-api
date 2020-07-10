import os
from sqlalchemy import Column, String, Integer, Boolean, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Task(db.Model):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    description = Column(String(120), nullable=False)
    important = Column(Boolean, nullable=False)
    urgent = Column(Boolean, nullable=False)
    done = Column(Boolean, nullable=False)
    sprint_id = Column(Integer, db.ForeignKey('sprint.id'), nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return {
            'id': self.id,
            'description': self.description,
            'important': self.important,
            'urgent': self.urgent,
            'done': self.done
        }


class Sprint(db.Model):
    __tablename__ = 'sprint'

    id = Column(Integer, primary_key=True)
    goal = Column(String(120), unique=True, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    tasks = db.relationship('Task', backref=db.backref('sprint', lazy='joined', cascade='delete-orphan'),
                            primaryjoin=id == Task.id)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return {
            'id': self.id,
            'goal': self.goal,
            'duration': self.duration
        }
