import pytest

from multichoice.forms import CreationMultiChoiceForm, MultiChoiceForm

### Test CreationMultiChoiceForm ###

def test_valid_create_mc_form():
    data = {
        "content": "question",
        "difficulty": 1,
        "order": 5,
        "theme1": None,
        "theme2": None,
        "theme3": None,
        "answer1": "a1",
        "answer1_correct": True,
        "answer2": "a2",
        "answer2_correct": False,
        "answer3": "a3",
        "answer3_correct": True,
    }
    form = CreationMultiChoiceForm(data)
    assert form.is_valid() is True

def test_invalid_create_mc_form():
    data = {
        "content": "question",
        "difficulty": 1,
        "order": 5,
        "theme1": None,
        "theme2": None,
        "theme3": None,
        "answer1": "",
        "answer1_correct": True,
        "answer2": "a2",
        "answer2_correct": False,
        "answer3": "a3",
        "answer3_correct": True,
    }
    form = CreationMultiChoiceForm(data)
    assert form.is_valid() is False


### Test MultiChoiceForm ###

def test_valid_mc_form():
    data = {
        "answer1": True,
        "answer2": False,
        "answer3": False,
        "qid": 1
    }
    form  =MultiChoiceForm(data)
    assert form.is_valid() is True

def test_invalid_mc_form():
    data = {
        "answer1": True,
        "answer2": False,
        "answer3": False,
        "qid": "str"
    }
    form  =MultiChoiceForm(data)
    assert form.is_valid() is False