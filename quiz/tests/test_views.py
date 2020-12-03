import datetime

import pytest
from pytest_django.asserts import assertTemplateUsed

from django.contrib.auth.models import User

from quiz.models import Category, SubCategory, Quiz


### FIXTURE ###

@pytest.fixture
def user_A(db):
    return User.objects.create_user(
        username="A",
        email="mail@mail.com",
        password="secret")

@pytest.fixture
def category_m(db):
    return Category.objects.create(category="m")

@pytest.fixture
def sub_category_n(db, category_m):
    return SubCategory.objects.create(category=category_m, sub_category="n")

@pytest.fixture
def quiz_q(db, category_m, sub_category_n, user_A):
    date = datetime.datetime.now()
    return Quiz.objects.create(
        title="title",
        description="Long description",
        creator=user_A,
        category=category_m,
        category_name="m",
        sub_category=sub_category_n,
        created=date,
        random_order=False,
        difficulty=1
    )


### Tests page tutorial ###

def test_page_tutorial_not_connected(client):
    response = client.get('/quiz/tutorial/')
    assert response.status_code == 200

def test_page_tutorial_connected(client, user_A):
    response = client.login(
        username=user_A.username,
        password=user_A.password
    )
    response = client.get('quiz/tutorial/')
    assert response.status_code == 200

### Tests page create ###

def test_access_page_create_unlogged(client):
    response = client.get("/quiz/create/")
    assert response.status_code == 302


def test_with_authenticated_client(client, django_user_model):
    user = User.objects.create_user("A")
    user.set_password("secret")
    client.force_login(user)
    response = client.get('/account/profile/')
    assert response.status_code == 200

### Test page load_sub_categories ###

def test_page_load_sub_categories(client):
    response = client.get('quiz/ajax/load-subcategories/')
    assert response.status_code == 200

### Test page quiz lists ###

def test_page_quiz_list(client, db):
    response = client.get('/quiz/quiz-list/')
    assert response.status_code == 200

def test_quiz_list_by_category(client, db):
    response = client.get('/quiz/category/Sciences/')
    assert response.status_code == 200

def test_quiz_list_by_subcategory(client, db):
    response = client.get('/quiz/subcategory/mathématiques/')
    assert response.status_code == 200


### Test page take ###

def test_take_quiz(client, quiz_q, user_A):
    client.force_login(user_A)
    url = '/quiz/take/' + quiz_q.url + '/'
    response = client.get(url)
    assert response.status_code == 200

### Test page statistics ###

def test_statistics(client, quiz_q, user_A):
    client.force_login(user_A)
    url = '/quiz/statistics/' + quiz_q.url + '/'
    response = client.get(url)
    assert response.status_code == 200