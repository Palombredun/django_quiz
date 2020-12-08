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

### Test profile ###

def test_profile(client, user_A):
	response = client.force_login(user_A)
	response = client.get('/users/profile/')

	assert response.status_code == 200
	assertTemplateUsed(response, "profiles/profile.html")