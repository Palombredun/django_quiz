import pytest
from pytest_django.asserts import assertTemplateUsed


def test_home(client, db):
    """
	GIVEN a user who wants to visit the home page
	WHEN he accesses the page
	THEN assert the right page is sent
	"""
    page = "/"

    response = client.get(page)

    assert response.status_code == 200
    assertTemplateUsed(response, "core/home.html")


def test_contact(client):
    """
	GIVEN a user who wants to visit the contact page
	WHEN he access the page
	THEN assert the right page is sent
	"""
    response = client.get("/contact/")

    assert response.status_code == 200
    assertTemplateUsed(response, "core/contact.html")


def test_license(client):
    """
	GIVEN a user who wants to visit the license page
	WHEN he access the page
	THEN assert the right page is sent
	"""
    response = client.get("/license/")

    assert response.status_code == 200
    assertTemplateUsed(response, "core/license.html")
