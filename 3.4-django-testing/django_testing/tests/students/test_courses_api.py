import pytest as pytest
from rest_framework.test import APIClient
from model_bakery import baker


from students.models import Student, Course


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory

# Проверка 1го курса
@pytest.mark.django_db
def test_one_course(client, course_factory, student_factory):
    course = course_factory(_quantity=1)

    # Act
    response = client.get('/api/v1/courses/')

    #Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(course)
    assert data[0]['name'] == course[0].name





# Проверка списка курсов
@pytest.mark.django_db
def test_courses_api(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=10)

    # Act
    response = client.get('/api/v1/courses/')

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)
    for i, c in enumerate(data):
        assert c['name'] == courses[i].name


# Проверка фильтров id
@pytest.mark.django_db
def test_filter_course(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=10)

    # Act
    response_courseid = client.get('/api/v1/courses/', {'id': 1})

    # Assert
    assert response_courseid.status_code == 200
    data_response_courseid = response_courseid.json()
    assert len(data_response_courseid) == 1
    assert data_response_courseid[0]['name'] == courses[0].name


# Проверка фильтра name
@pytest.mark.django_db
def test_filter_course(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=10)

    # Act
    response_coursename = client.get('/api/v1/courses/', {'name': courses[0].name})

    # Assert
    assert response_coursename.status_code == 200
    data_response_coursename = response_coursename.json()
    assert len(data_response_coursename) == 1
    assert data_response_coursename[0]['name'] == courses[0].name


# тест создания нового курса
@pytest.mark.django_db
def test_create_course(client):
    # Arrange
    count = Course.objects.count()

    # Act
    response = client.post('/api/v1/courses/', data={'name': 'test text'})

    # Assert
    assert response.status_code == 201
    assert Course.objects.count() == count + 1


# тест обновления курса
@pytest.mark.django_db
def test_update_course(client, course_factory):
    # Arrange
    count = Course.objects.count()
    course = course_factory(_quantity=1)

    # Act
    updated_data = {'name': 'updated text'}
    response = client.patch(f'/api/v1/courses/{Course.objects.first().id}/', updated_data)

    # Assert
    data = response.json()
    assert response.status_code == 200
    assert data['name'] == updated_data['name']
    assert Course.objects.count() == count + 1


# тест удаления курса
@pytest.mark.django_db
def test_del_course(client, course_factory):
    # Arrange
    course = course_factory(_quantity=1)

    # Act
    response = client.delete(f'/api/v1/courses/{Course.objects.first().id}/')

    # Assert
    assert response.status_code == 204
    assert Course.objects.count() == 0