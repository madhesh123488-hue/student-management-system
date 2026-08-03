from flask import redirect, url_for

STUDENT_FIELDS = (
    ('name', 'Name'),
    ('roll', 'Roll No'),
    ('course', 'Course'),
)


def parse_student_form(form):
    return {key: form[key] for key, _ in STUDENT_FIELDS}


def redirect_home():
    return redirect(url_for('index'))
