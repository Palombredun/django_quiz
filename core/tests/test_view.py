import pytest
from pytest_django.asserts import assertTemplateUsed

def test_home(client, db):
	response = client.get('/')
	assert response.status_code == 200
	assertTemplateUsed(response, 'core/home.html')