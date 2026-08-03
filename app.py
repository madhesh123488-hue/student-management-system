import logging
import os

from flask import Flask, abort, flash, jsonify, redirect, render_template, request
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')

logging.basicConfig(level=logging.INFO)

students = []

FIELDS = ('name', 'roll', 'course')


@app.route('/')
def index():
    return render_template('index.html', students=students)


@app.route('/add', methods=['POST'])
def add_student():
    student = {}
    missing = []
    for field in FIELDS:
        value = (request.form.get(field) or '').strip()
        if not value:
            missing.append(field)
        student[field] = value

    if missing:
        message = 'Missing required field(s): {}'.format(', '.join(missing))
        app.logger.warning('Rejected add_student request: %s', message)
        flash(message, 'error')
        return render_template('index.html', students=students), 400

    if any(existing['roll'] == student['roll'] for existing in students):
        message = 'A student with roll no {} already exists.'.format(student['roll'])
        app.logger.warning('Rejected add_student request: %s', message)
        flash(message, 'error')
        return render_template('index.html', students=students), 400

    students.append(student)
    app.logger.info('Added student with roll no %s', student['roll'])
    flash('Added {}.'.format(student['name']), 'success')
    return redirect('/')


@app.route('/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    if student_id < 0 or student_id >= len(students):
        app.logger.warning('Rejected delete for unknown student index %s', student_id)
        abort(404, description='No student exists at position {}.'.format(student_id))

    student = students.pop(student_id)
    app.logger.info('Deleted student with roll no %s', student['roll'])
    flash('Deleted {}.'.format(student['name']), 'success')
    return redirect('/')


@app.errorhandler(HTTPException)
def handle_http_exception(error):
    app.logger.warning('HTTP %s on %s: %s', error.code, request.path, error.description)
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return jsonify(error=error.name, message=error.description), error.code
    return render_template('error.html', code=error.code, name=error.name,
                           message=error.description), error.code


@app.errorhandler(Exception)
def handle_unexpected_exception(error):
    app.logger.exception('Unhandled error on %s', request.path)
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return jsonify(error='Internal Server Error',
                       message='An unexpected error occurred.'), 500
    return render_template('error.html', code=500, name='Internal Server Error',
                           message='An unexpected error occurred.'), 500


if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', '').lower() in ('1', 'true', 'yes'))
