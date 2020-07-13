from datetime import datetime
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Task, Sprint


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/sprints', methods=['GET'])
    def get_sprints():
        sprints = [sprint.short() for sprint in Sprint.query.all()]

        return jsonify({
            'success': True,
            'sprints': sprints
        })

    @app.route('/sprints', methods=['POST'])
    def post_sprints():
        payload = get_sprint_payload()

        sprint = Sprint(
            goal=payload['goal'],
            start_date=payload['start_date'],
            end_date=payload['end_date']
        )
        sprint.insert()

        return jsonify({
            'success': True,
            'sprint': sprint.short()
        })

    @app.route('/sprints/<int:sprint_id>', methods=['PATCH'])
    def patch_sprints(sprint_id):
        payload = get_sprint_payload()

        sprint = Sprint.query.get(sprint_id)
        if payload['goal'] is not None:
            sprint.goal = payload['goal']
        if payload['start_date'] is not None:
            sprint.start_date = payload['start_date']
        if payload['end_date'] is not None:
            sprint.end_date = payload['end_date']
        sprint.update()

        return jsonify({
            'success': True,
            'sprint': sprint.short()
        })

    @app.route('/sprints/<int:sprint_id>', methods=['DELETE'])
    def delete_sprints(sprint_id):
        sprint = Sprint.query.get(sprint_id)
        sprint.delete()

        return jsonify({
            'success': True,
            'sprint_deleted': sprint_id
        })

    def get_sprint_payload():
        body = request.get_json()
        goal = body.get('goal', None)
        start_date = body.get('start_date', None)
        end_date = body.get('end_date', None)

        return {
            'goal': goal,
            'end_date': to_date(end_date) if end_date is not None else None,
            'start_date': to_date(start_date) if start_date is not None else None
        }

    def to_date(new_end_date):
        return datetime.strptime(new_end_date, '%Y-%m-%d')

    @app.route('/sprints/<int:sprint_id>/tasks', methods=['GET'])
    def get_tasks(sprint_id):
        tasks = [task.short() for task in Task.query.filter_by(sprint_id=sprint_id)]

        return jsonify({
            'success': True,
            'tasks': tasks
        })

    @app.route('/sprints/<int:sprint_id>/tasks', methods=['POST'])
    def post_tasks(sprint_id):
        payload = get_task_payload()

        task = Task(
            description=payload['description'],
            important=payload['important'],
            urgent=payload['urgent'],
            done=payload['done'],
            sprint_id=sprint_id
        )
        task.insert()

        return jsonify({
            'success': True,
            'task': task.short()
        })

    @app.route('/tasks/<int:task_id>', methods=['PATCH'])
    def patch_tasks(task_id):
        payload = get_task_payload()

        task = Task.query.get(task_id)
        if payload['description'] is not None:
            task.description = payload['description']
        if payload['important'] is not None:
            task.important = payload['important']
        if payload['urgent'] is not None:
            task.urgent = payload['urgent']
        if payload['done'] is not None:
            task.done = payload['done']

        task.update()

        return jsonify({
            'success': True,
            'task': task.short()
        })

    @app.route('/tasks/<int:task_id>', methods=['DELETE'])
    def delete_tasks(task_id):
        task = Task.query.get(task_id)
        task.delete()

        return jsonify({
            'success': True,
            'deleted_task': task_id
        })

    def get_task_payload():
        body = request.get_json()
        return {
            'description': body.get('description', None),
            'important': body.get('important', None),
            'urgent': body.get('urgent', None),
            'done': body.get('done', None)
        }

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
