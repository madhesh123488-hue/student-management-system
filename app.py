from flask import Flask, render_template, request

from utils import STUDENT_FIELDS, parse_student_form, redirect_home

app = Flask(__name__)

students = []

@app.route('/')
def index():
    return render_template('index.html', students=students, fields=STUDENT_FIELDS)

@app.route('/add', methods=['POST'])
def add_student():
    students.append(parse_student_form(request.form))
    return redirect_home()

@app.route('/delete/<int:student_id>')
def delete_student(student_id):
    students.pop(student_id)
    return redirect_home()

if __name__ == '__main__':
    app.run(debug=True)
