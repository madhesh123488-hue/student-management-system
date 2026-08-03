import os

from flask import Flask, abort, render_template, request, redirect

app = Flask(__name__)

MAX_FIELD_LENGTH = 100

students = []


def _clean_field(name):
    value = request.form.get(name, '').strip()
    if not value or len(value) > MAX_FIELD_LENGTH:
        abort(400)
    return value


@app.route('/')
def index():
    return render_template('index.html', students=students)


@app.route('/add', methods=['POST'])
def add_student():
    student = {field: _clean_field(field) for field in ('name', 'roll', 'course')}
    students.append(student)
    return redirect('/')


@app.route('/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    if student_id >= len(students):
        abort(404)
    students.pop(student_id)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG') == '1')
