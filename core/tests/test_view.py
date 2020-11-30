import pytest
from pytest_django.asserts import assertTemplateUsed

@pytest.mark.django_db
def test_home(client):
	response = client.get('/')
	assert response.status_code == 200
	assertTemplateUsed(response, 'core/home.html')