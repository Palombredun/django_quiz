import datetime

import pytest

from django.contrib.auth.models import User

from quiz.models import Category, Quiz
from multichoice.models import MCQuestion

### Fixtures ###

@pytest.fixture
def category_m(db):
    return Category.objects.create(category="m")


@pytest.fixture
def user_A(db):
    return User.objects.create_user(username="A")


@pytest.fixture
def quiz_q(db, category_m, user_A):
    date = datetime.datetime.now()
    return Quiz.objects.create(
        title="title",
        description="Long description",
        creator=user_A,
        category=category_m,
        category_name="m",
        sub_category=None,
        created=date,
        random_order=False,
        difficulty=1,
    )

@pytest.fixture
def mc_question_one_true(quiz_q):
    return MCQuestion.objects.create(
        quiz=quiz_q,
        difficulty=1,
        order=1,
        figure=None,
        content="mc",
        explanation="",
        theme1="t1",
        theme2="t2",
        theme3="t3",
        answer1="a1",
        answer1_correct=True,
        answer2="a2",
        answer2_correct=False,
        answer3="a3",
        answer3_correct=False,
    )

@pytest.fixture
def mc_question_all_true(quiz_q):
    return MCQuestion.objects.create(
        quiz=quiz_q,
        difficulty=1,
        order=1,
        figure=None,
        content="mc",
        explanation="",
        theme1="t1",
        theme2="t2",
        theme3="t3",
        answer1="a1",
        answer1_correct=True,
        answer2="a2",
        answer2_correct=True,
        answer3="a3",
        answer3_correct=True,
    )

### Test model MCQuestion ###
def test_model_mc_question(mc_question_one_true):
    """
    GIVEN a MultiChoiceQuestion with valid data
    WHEN this data has to be compared
    THEN assert it returns what is expected
    """
    assert mc_question_one_true.answer1 == "a1"
    assert mc_question_one_true.answer1_correct == True
    assert mc_question_one_true.answer2 == "a2"
    assert mc_question_one_true.answer2_correct == False
    assert mc_question_one_true.answer3 == "a3"
    assert mc_question_one_true.answer3_correct == False

def test_model_mc_question_all_true(mc_question_all_true):
    """
    GIVEN a MultiChoiceQuestion where all questions are True
    WHEN this data has to be compared
    THEN assert it returns what is expected
    """
    assert mc_question_all_true.answer1_correct == True
    assert mc_question_all_true.answer2_correct == True
    assert mc_question_all_true.answer3_correct == True