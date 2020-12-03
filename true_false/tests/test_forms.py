import pytest

from true_false.forms import CreationTrueFalseForm, TrueFalseForm


def test_valid_creation_form():
    data = {
        "content": "question",
        "difficulty": 1,
        "order": 2,
        "theme1": "t1",
        "theme2": "t2",
        "theme3": "t3",
        "correct": True,
    }
    form = CreationTrueFalseForm(data)
    assert form.is_valid() is True


def test_invalid_creation_form():
    data = {
        "content": "",
        "difficulty": 1,
        "order": 2,
        "theme1": "t1",
        "theme2": "t2",
        "theme3": "t3",
        "correct": True,
    }
    form = CreationTrueFalseForm(data)
    assert form.is_valid() is False


def test_valid_creation_form_without_theme():
    data = {
        "content": "question",
        "difficulty": 1,
        "order": 2,
        "theme1": "",
        "theme2": "",
        "theme3": "",
        "correct": True,
    }
    form = CreationTrueFalseForm(data)
    assert form.is_valid() is True


def test_valid_true_false_form():
	data = {
		"correct": True,
		"qid": 1
	}
	form = TrueFalseForm(data)
	assert form.is_valid() is True

def test_invalid_true_false_form():
	data = {
		"correct": None,
		"qid": 1
	}
	form = TrueFalseForm(data)
	assert form.is_valid() is False