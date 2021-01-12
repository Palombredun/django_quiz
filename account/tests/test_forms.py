import pytest

from django import forms

from account.forms import UserRegistrationForm

def test_valid_user_creation_form(db):
	"""
	GIVEN the data of a valid user
	WHEN UserRegistrationForm is given this data
	THEN assert it returns True when is_valid() is called
	"""
	data = {
		"username": "toto",
		"email": "mail@mail.com",
		"password": "secret",
		"password2": "secret"
	}

	form = UserRegistrationForm(data)

	assert form.is_valid() is True

def test_invalid_user_creation_form(db):
	"""
	GIVEN the data of a user with a wrong email adreess
	WHEN UserRegistrationForm is given this data
	THEN assert is_valid() returns False when it is called
	"""
	data = {
		"username": "toto",
		"email": "mymail",
		"password": "secret",
		"password": "secret"
	}

	form = UserRegistrationForm(data)

	assert form.is_valid() is False

def test_different_passwords_user_creation_form(db):
	"""
	GIVEN the data of a user where passwords don't match
	WHEN UserRegistrationForm is given this data
	THEN assert it returns False when is_valid() is called
	"""
	data = {
		"username": "toto",
		"email": "mail@mail.com",
		"password": "secret1",
		"password2": "secret2"
	}

	form = UserRegistrationForm(data)
	
	assert form.is_valid() is False
	