import pytest


def add(client, name='Ada', roll='1', course='Math'):
    return client.post('/add', data={'name': name, 'roll': roll, 'course': course})


class TestIndex:
    def test_renders_empty_list(self, client):
        response = client.get('/')
        body = response.get_data(as_text=True)
        assert response.status_code == 200
        assert 'Student Management System' in body
        assert 'delete-btn' not in body

    def test_renders_students(self, client, students):
        students.append({'name': 'Ada', 'roll': '1', 'course': 'Math'})
        students.append({'name': 'Alan', 'roll': '2', 'course': 'Logic'})

        body = client.get('/').get_data(as_text=True)

        assert 'Ada' in body and 'Math' in body
        assert 'Alan' in body and 'Logic' in body
        assert '/delete/0' in body
        assert '/delete/1' in body

    def test_escapes_student_values(self, client, students):
        students.append({'name': '<script>x</script>', 'roll': '1', 'course': 'Math'})

        body = client.get('/').get_data(as_text=True)

        assert '<script>x</script>' not in body
        assert '&lt;script&gt;' in body


class TestAddStudent:
    def test_appends_student_and_redirects(self, client, students):
        response = add(client, 'Ada', '1', 'Math')

        assert response.status_code == 302
        assert response.headers['Location'] == '/'
        assert students == [{'name': 'Ada', 'roll': '1', 'course': 'Math'}]

    def test_preserves_insertion_order(self, client, students):
        add(client, 'Ada', '1', 'Math')
        add(client, 'Alan', '2', 'Logic')

        assert [s['name'] for s in students] == ['Ada', 'Alan']

    def test_allows_duplicate_roll_numbers(self, client, students):
        add(client, 'Ada', '1', 'Math')
        add(client, 'Alan', '1', 'Logic')

        assert len(students) == 2

    def test_accepts_empty_string_fields(self, client, students):
        add(client, '', '', '')

        assert students == [{'name': '', 'roll': '', 'course': ''}]

    @pytest.mark.parametrize('missing', ['name', 'roll', 'course'])
    def test_missing_field_is_a_bad_request(self, client, students, missing):
        data = {'name': 'Ada', 'roll': '1', 'course': 'Math'}
        del data[missing]

        response = client.post('/add', data=data)

        assert response.status_code == 400
        assert students == []

    def test_rejects_get(self, client):
        assert client.get('/add').status_code == 405

    def test_follow_redirect_shows_new_student(self, client):
        response = add(client, 'Ada', '1', 'Math')
        body = client.get(response.headers['Location']).get_data(as_text=True)

        assert 'Ada' in body


class TestDeleteStudent:
    def test_removes_student_and_redirects(self, client, students):
        add(client, 'Ada', '1', 'Math')

        response = client.get('/delete/0')

        assert response.status_code == 302
        assert response.headers['Location'] == '/'
        assert students == []

    def test_removes_only_the_requested_index(self, client, students):
        add(client, 'Ada', '1', 'Math')
        add(client, 'Alan', '2', 'Logic')
        add(client, 'Grace', '3', 'Compilers')

        client.get('/delete/1')

        assert [s['name'] for s in students] == ['Ada', 'Grace']

    def test_out_of_range_index_raises(self, client, students):
        with pytest.raises(IndexError):
            client.get('/delete/0')

    def test_non_integer_index_is_not_found(self, client):
        assert client.get('/delete/abc').status_code == 404

    def test_negative_index_is_not_found(self, client):
        assert client.get('/delete/-1').status_code == 404
