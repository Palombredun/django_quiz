import datetime

import pytest

from django.contrib.auth.models import User

from quiz.models import Category, Quiz
from true_false.models import TF_Question

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
def true_false_true(quiz_q):
    return TF_Question.objects.create(
        quiz=quiz_q,
        difficulty=1,
        order=1,
        figure=None,
        content="question",
        explanation=None,
        theme1="t1",
        theme2="t2",
        theme3="t3",
        correct=True,
    )


@pytest.fixture
def true_false_false(quiz_q):
    return TF_Question.objects.create(
        quiz=quiz_q,
        difficulty=1,
        order=1,
        figure=None,
        content="question",
        explanation=None,
        theme1="t1",
        theme2="t2",
        theme3="t3",
        correct=False,
    )


## Test TF_Question ###


def test_true_false_question_model_true(true_false_true):
    """
    GIVEN a TF_Question model
    WHEN an instance of it with correct set to True and is saved
    THEN assert it has been correctly saved
    """
    assert true_false_true.correct == True


def test_true_false_question_model_false(true_false_false):
    """
    GIVEN a TF_Question model
    WHEN an instance of it with correct set to False and is saved
    THEN assert it has been correctly saved
    """
    assert true_false_false.correct == False
