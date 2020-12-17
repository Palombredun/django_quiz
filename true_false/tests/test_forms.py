import pytest

from true_false.forms import CreationTrueFalseForm, TrueFalseForm


def test_valid_creation_form():
    """
    GIVEN data representing a valid CreationTrueFalseForm
    WHEN it is given to CreationTrueFalseForm
    THEN assert is_valid() returns True
    """
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
    """
    GIVEN data representing an invalid CreationTrueFalseForm
    WHEN it is given to CreationTrueFalseForm
    THEN assert is_valid() returns False
    """
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
    """
    GIVEN the data representing a valid CreationTrueFalseForm without theme
    WHEN it is given to CreationTrueFalseForm
    THEN assert is_valid() returns True
    """
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
    """
    GIVEN the data representing a valid TrueFalseForm
    WHEN it is given to TrueFalseForm
    THEN assert is_valid() returns True
    """
	data = {
		"correct": True,
		"qid": 1
	}

	form = TrueFalseForm(data)

	assert form.is_valid() is True

def test_invalid_true_false_form():
    """
    GIVEN the data representing an invalid TrueFalseForm
    WHEN it is given to TrueFalseForm
    THEN assert is_valid() returns False
    """
	data = {
		"correct": None,
		"qid": 1
	}
	form = TrueFalseForm(data)
	assert form.is_valid() is False