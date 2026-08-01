from flask import Flask, render_template, request, redirect

app = Flask(__name__)

students = []

@app.route('/')
def index():
    return render_template('index.html', students=students)

@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    roll = request.form['roll']
    course = request.form['course']
    students.append({'name': name, 'roll': roll, 'course': course})
    return redirect('/')

@app.route('/delete/<int:student_id>')
def delete_student(student_id):
    students.pop(student_id)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
