import pytest

from django import forms

from account.forms import UserRegistrationForm

def test_valid_user_creation_form(db):
	data = {
		"username": "toto",
		"email": "mail@mail.com",
		"password": "secret",
		"password2": "secret"
	}
	form = UserRegistrationForm(data)
	assert form.is_valid() is True

def test_invalid_user_creation_form(db):
	data = {
		"username": "toto",
		"email": "mymail",
		"password": "secret",
		"password": "secret"
	}
	form = UserRegistrationForm(data)

	assert form.is_valid() is False

def test_different_passwords_user_creation_form(db):
	data = {
		"username": "toto",
		"email": "mail@mail.com",
		"password": "secret1",
		"password2": "secret2"
	}
	form = UserRegistrationForm(data)
	assert form.is_valid() is False