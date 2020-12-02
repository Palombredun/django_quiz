import pytest

from quiz.forms import QuestionForm, QuizForm

def test_valid_questionForm():
	data = {
		'content': "question",
		'difficulty': 1,
		'theme1': 't1',
		'theme2': 't2',
		'theme3': 't3',
		'order': 1
	}
	form = QuestionForm(data)
	assert form.is_valid() is True

def test_invalid_questionForm():
	data = {
		'content': "",
		'difficulty': 1,
		'theme1': 't1',
		'theme2': 't2',
		'theme3': 't3',
		'order': 1
	}
	form = QuestionForm(data)
	assert form.is_valid() is False

def test_valid_quizForm():
	data = {
		'title': "titre",
		'description': 'Lorem ipsum',
		'category': 1,
		'sub_category': 1,
		'random_order': False
	}
	form = QuizForm(data)
	assert form.is_valid() is True

def test_invalid_quizForm():
	data = {
		'title': "",
		'description': 'Lorem ipsum',
		'category': 1,
		'sub_category': 1,
		'random_order': False
	}
	form = QuizForm(data)
	assert form.is_valid() is False