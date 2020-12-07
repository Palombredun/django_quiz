import pytest
from pytest_django.asserts import assertTemplateUsed

from django.contrib import auth
from django.contrib.auth.models import User


### Fixture


@pytest.fixture
def user_A(db):
    return User.objects.create_user(
        username="A", email="mail@mail.com", password="secret"
    )


# Test register


def test_register(client):
    """
    GIVEN a user who wants to create an account
    WHEN he visits the register page
    THEN assert he gets the good page
    """
    page = "/account/register/"

    response = client.get(page)

    assert response.status_code == 200
    assertTemplateUsed(response, "account/register.html")


def test_create_user(user_A):
    """
    GIVEN a user created with a username and an email
    WHEN the execute method is called
    THEN assert a new User exists with the corresponding properties
    """
    assert user_A.username == "A"
    assert user_A.email == "mail@mail.com"


def test_should_check_password(user_A):
    """
    GIVEN a user created with a user and an email
    WHEN his password is set
    THEN assert the good password has been saved
    """
    user_A.set_password("secret")

    assert user_A.check_password("secret") is True


def test_should_not_check_unsuable_password(db, user_A):
    """
    GIVEN a user created whith an unusable password
    WHEN his password is checked
    THEN assert the check fails
    """
    user_A.set_password("secret")
    user_A.set_unusable_password()

    assert user_A.check_password("secret") is False


# test login


def test_login_page(client):
    """
    GIVEN a user who wants to login
    WHEN he access the page
    THEN assert the good page is sent
    """
    response = client.get("/account/login/")

    assert response.status_code == 200
    assertTemplateUsed(response, "registration/login.html")


def test_login_with_username(client, user_A):
    """
    GIVEN a user who uses the login page to connect
    WHEN he post his credentials
    THEN assert his is correctly logged
    """
    data = {"username": user_A.username, "password": user_A.password}

    response = client.post("/account/login/", data)

    assert response.status_code == 200
    response = client.get("/account/profile/")
    assert response.status_code == 200


def test_login_with_email(client, user_A):
    """
    GIVEN a user who wants to login using his email as identifier
    WHEN he posts his credentials
    THEN assert he is properly logged in
    """
    data = {"username": user_A.email, "password": user_A.password}

    response = client.post("/account/login/")

    assert response.status_code == 200
    response = client.get("/account/profile/")
    assert response.status_code == 200


def test_login_with_wrong_password(client, user_A):
    """
    GIVEN a user who tries to login with the wrong password
    WHEN he posts his credentials
    THEN assert he is not logged in
    """
    response = client.login(username=user_A.username, password="zzz")
    assert response == False


def test_login_with_wrong_username(client, user_A):
    """
    GIVEN a user who tries to login with the wrong username
    WHEN he posts his credentials
    THEN assert he is not logged in
    """
    response = client.login(username="Z", password=user_A.password)
    assert response == False


# Test logout


def test_logout(client, user_A):
    """
    GIVEN a logged in user
    WHEN he uses the logout page
    THEN assert he is properly logged out
    """
    response = client.login(username=user_A.username, password=user_A.password)
    response = client.get("/account/logout/")
    assert response.status_code == 302
