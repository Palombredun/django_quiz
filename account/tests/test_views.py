import pytest

from django.contrib import auth
from django.contrib.auth.models import User


### Fixture

@pytest.fixture
def user_A(db):
    return User.objects.create_user(
        username="A",
        email="mail@mail.com",
        password="secret")

# Test register

def test_register(client):
    response = client.get('/account/register/')
    assert response.status_code == 200

def test_create_user(db, user_A):
    assert user_A.username == "A"
    assert user_A.email == "mail@mail.com"

def test_should_check_password(db, user_A):
    user_A.set_password("secret")
    assert user_A.check_password("secret") is True

def test_should_not_check_unsuable_password(db, user_A):
    user_A.set_password("secret")
    user_A.set_unusable_password()
    assert user_A.check_password("secret") is False


# test login

def test_login_page(client):
    response = client.get('/account/login/')
    assert response.status_code == 200

def test_login_with_username(client, user_A):
    response = client.post('/account/login/', 
        {'username': user_A.username,
        'password': user_A.password,
    })
    assert response.status_code == 200
    response = client.get('/account/profile/')
    assert response.status_code == 200

def test_login_with_email(client, user_A):
    response = client.post('/account/login/', 
        {'username': user_A.email,
        'password': user_A.password,
    })
    assert response.status_code == 200
    response = client.get('/account/profile/')
    assert response.status_code == 200

def test_login_with_wrong_password(client, user_A):
    response = client.login(
        username=user_A.username,
        password="zzz")
    assert response == False

# Test logout

def test_logout(client, user_A):
    response = client.login(
        username=user_A.username,
        password=user_A.password
    )
    response = client.get('/account/logout/')
    assert response.status_code == 302