import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Task, String


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/sprints', methods=['GET'])
    def get_sprints():
        return jsonify({'success': True})

    @app.route('/sprints', methods=['POST'])
    def post_sprints():
        return jsonify({'success': True})

    @app.route('/sprints/<int:sprint_id>', methods=['PATCH'])
    def patch_sprints(sprint_id):
        return jsonify({'success': True})

    @app.route('/sprints/<int:sprint_id>', methods=['DELETE'])
    def delete_sprints(sprint_id):
        return jsonify({'success': True})

    @app.route('/sprints/<int:sprint_id>/tasks', methods=['GET'])
    def get_tasks(sprint_id):
        return jsonify({'success': True})

    @app.route('/sprints/<int:sprint_id>/tasks', methods=['POST'])
    def post_tasks(sprint_id):
        return jsonify({'success': True})

    @app.route('/tasks/<int:task_id>', methods=['PATCH'])
    def patch_tasks(task_id):
        return jsonify({'success': True})

    @app.route('/tasks/<int:task_id>', methods=['DELETE'])
    def delete_tasks(task_id):
        return jsonify({'success': True})

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
