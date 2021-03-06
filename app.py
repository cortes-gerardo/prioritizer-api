from datetime import datetime
import os
from flask import Flask, render_template, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Task, Sprint
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST,PATCH,DELETE')
        return response

    # Controllers
    @app.route('/')
    def index():
        sprints = [sprint.short() for sprint in Sprint.query.all()]
        return render_template(
            'pages/home.html',
            nav='home',
            sprints=sprints
        )

    @app.route('/sprints/<int:sprint_id>', methods=['GET'])
    def select_sprint(sprint_id):
        sprints = [sprint.short() for sprint in Sprint.query.all()]
        necessity = classify_tasks(sprint_id, True, True)
        productivity = classify_tasks(sprint_id, True, False)
        distraction = classify_tasks(sprint_id, False, True)
        waste = classify_tasks(sprint_id, False, False)

        return render_template(
            'pages/home.html',
            nav='home',
            sprints=sprints,
            sprint_selected=sprint_id,
            necessity=necessity,
            productivity=productivity,
            distraction=distraction,
            waste=waste
        )

    @app.route('/authorize')
    def authorize():
        return render_template('pages/authorize.html', nav='auth')

    @app.route('/sprints', methods=['GET'])
    def get_sprints():
        sprints = [sprint.short() for sprint in Sprint.query.all()]

        return jsonify({
            'success': True,
            'sprints': sprints
        })

    @app.route('/sprints', methods=['POST'])
    @requires_auth('post:sprint')
    def post_sprints():
        payload = get_sprint_payload()

        check_valid_sprint_post_payload(payload)
        check_goal_does_not_exist_already(payload)

        sprint = Sprint(
            goal=payload['goal'],
            start_date=payload['start_date'],
            end_date=payload['end_date']
        )
        sprint.insert()

        return jsonify({
            'success': True,
            'sprint': sprint.short()
        }), 201

    @app.route('/sprints/<int:sprint_id>', methods=['PATCH'])
    @requires_auth('patch:sprint')
    def patch_sprints(sprint_id):
        payload = get_sprint_payload()

        check_sprint_exist(sprint_id)
        check_valid_sprint_patch_payload(payload)
        check_goal_does_not_exist_already(payload)

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
    @requires_auth('delete:sprint')
    def delete_sprints(sprint_id):
        check_sprint_exist(sprint_id)

        sprint = Sprint.query.get(sprint_id)
        sprint.delete()

        return jsonify({
            'success': True,
            'deleted_sprint': sprint_id
        })

    @app.route('/sprints/<int:sprint_id>/tasks', methods=['GET'])
    def get_tasks(sprint_id):
        check_sprint_exist(sprint_id)

        necessity = classify_tasks(sprint_id, True, True)
        productivity = classify_tasks(sprint_id, True, False)
        distraction = classify_tasks(sprint_id, False, True)
        waste = classify_tasks(sprint_id, False, False)

        return jsonify({
            'success': True,
            'necessity': necessity,
            'productivity': productivity,
            'distraction': distraction,
            'waste': waste
        })

    @app.route('/sprints/<int:sprint_id>/tasks', methods=['POST'])
    @requires_auth('post:task')
    def post_tasks(sprint_id):
        payload = get_task_payload()
        check_sprint_exist(sprint_id)
        check_valid_post_task_payload(payload)

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
        }), 201

    @app.route('/tasks/<int:task_id>', methods=['PATCH'])
    @requires_auth('patch:task')
    def patch_tasks(task_id):
        payload = get_task_payload()

        check_valid_patch_task_payload(payload)
        check_task_exist(task_id)

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
    @requires_auth('delete:task')
    def delete_tasks(task_id):
        check_task_exist(task_id)

        task = Task.query.get(task_id)
        task.delete()

        return jsonify({
            'success': True,
            'deleted_task': task_id
        })

    # helpers

    def classify_tasks(id, i, u):
        return [task.short() for task in
                Task.query.filter_by(
                    sprint_id=id,
                    important=i,
                    urgent=u
                )]

    def get_task_payload():
        body = request.get_json()
        return {
            'description': body.get('description', None),
            'important': body.get('important', None),
            'urgent': body.get('urgent', None),
            'done': body.get('done', None)
        }

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
        # todo if can't be parsed, then abort(400)
        return datetime.strptime(new_end_date, '%Y-%m-%d')

    def check_valid_sprint_patch_payload(payload):
        if payload['goal'] is None \
                and payload['start_date'] is None \
                and payload['end_date'] is None:
            abort(400)

    def check_valid_post_task_payload(payload):
        if payload['description'] is None \
                or payload['important'] is None \
                or payload['urgent'] is None \
                or payload['done'] is None:
            abort(400)

    def check_valid_patch_task_payload(payload):
        if payload['description'] is None \
                and payload['important'] is None \
                and payload['urgent'] is None \
                and payload['done'] is None:
            abort(400)

    def check_sprint_exist(sprint_id):
        if Sprint.query.filter_by(id=sprint_id).count() <= 0:
            abort(404)

    def check_task_exist(task_id):
        if Task.query.filter_by(id=task_id).count() <= 0:
            abort(404)

    def check_valid_sprint_post_payload(payload):
        if payload['goal'] is None \
                or payload['start_date'] is None \
                or payload['end_date'] is None:
            abort(400)

    def check_goal_does_not_exist_already(payload):
        if Sprint.query.filter_by(goal=payload['goal']).count() > 0:
            abort(422)

    # Error Handling

    @app.errorhandler(AuthError)
    def handle_auth_error(error):
        message = {
            400: 'Bad Request',
            401: 'Unauthorized',
            403: 'Forbidden'
        }
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": message[error.status_code],
            "code": error.error['code'],
            "description": error.error['description']
        }), error.status_code

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='127.0.0.1', port=8080, debug=True)
