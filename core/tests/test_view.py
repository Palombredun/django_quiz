import pytest
from pytest_django.asserts import assertTemplateUsed

def test_home(client, db):
	response = client.get('/')
	assert response.status_code == 200
	assertTemplateUsed(response, 'core/home.html')

def test_contact(client):
	response = client.get('/contact/')
	assert response.status_code == 200
	assertTemplateUsed(response, 'core/contact.html')

def test_license(client):
	response = client.get('/license/')
	assert response.status_code == 200
	assertTemplateUsed(response, 'core/license.html')