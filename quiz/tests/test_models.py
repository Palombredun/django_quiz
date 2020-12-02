import datetime

from django.contrib.auth.models import User

from quiz.models import (
    AnswerUser, 
    Category, 
    Grade, 
    Question,
    QuestionScore,
    Quiz, 
    Statistic, 
    SubCategory,
    ThemeScore
    )

import pytest


### FIXTURES ###

@pytest.fixture
def category_m(db):
    return Category.objects.create(category="m")

@pytest.fixture
def sub_category_n(db, category_m):
    return SubCategory.objects.create(category=category_m, sub_category="n")

@pytest.fixture
def user_A(db):
    return User.objects.create_user(username="A")

@pytest.fixture
def quiz_q(db, category_m, sub_category_n, user_A):
    date = datetime.datetime.now()
    return Quiz.objects.create(
        title="title",
        description="Long description",
        creator=user_A,
        category=category_m,
        category_name="m",
        sub_category=sub_category_n,
        created=date,
        random_order=False,
        difficulty=1
        )

@pytest.fixture
def question_q(db, quiz_q):
    return Question.objects.create(
        quiz=quiz_q,
        difficulty=1,
        order=1,
        figure=None,
        content="question",
        explanation=None,
        theme1="t1",
        theme2="t2",
        theme3="t3",
        )

@pytest.fixture
def answerUser(db, question_q, user_A):
    a = AnswerUser.objects.create(correct=True)
    a.save()
    a.question.add(question_q)
    a.user.add(user_A)
    return a

@pytest.fixture
def stats_s(db, quiz_q):
    return Statistic.objects.create(
        quiz=quiz_q,
        number_participants=10,
        mean=15,
        easy=5,
        medium=5,
        difficult=5
    )

@pytest.fixture
def grade_g(db, stats_s):
    return Grade.objects.create(grade=5, number=10, statistics=stats_s)

@pytest.fixture
def questionScore_qs(db, stats_s, question_q):
    return QuestionScore.objects.create(
        question=question_q,
        statistics=stats_s,
        score=5
    )

@pytest.fixture
def themeScore_ts(db, stats_s, quiz_q):
    return ThemeScore.objects.create(
        theme="t1",
        score=5,
        statistics=stats_s,
        quiz=quiz_q
    )

### TESTS ###

def test_category(category_m):
    assert isinstance(category_m, Category)
    assert category_m.category == "m"

def test_sub_category(category_m, sub_category_n):
    assert sub_category_n.sub_category == "n"
    assert sub_category_n.category == category_m
    assert isinstance(sub_category_n, SubCategory)

def test_quiz(quiz_q, user_A, category_m, sub_category_n):
    date = datetime.datetime.now()
    assert quiz_q.title == "title"
    assert quiz_q.description == "Long description"
    assert quiz_q.creator == user_A
    assert quiz_q.category == category_m
    assert quiz_q.sub_category == sub_category_n
    assert isinstance(quiz_q.created, datetime.datetime)
    assert quiz_q.created.year == date.year
    assert quiz_q.created.month == date.month
    assert quiz_q.created.day == date.day
    assert quiz_q.created.hour == date.hour
    assert quiz_q.created.minute == date.minute
    assert quiz_q.created.second == date.second
    assert quiz_q.random_order == False
    assert quiz_q.difficulty == 1

def test_question(quiz_q, question_q):
    assert question_q.quiz == quiz_q
    assert question_q.difficulty == 1
    assert question_q.order == 1
    assert question_q.figure == None
    assert question_q.content == "question"
    assert question_q.explanation == None
    assert question_q.theme1 == "t1"
    assert question_q.theme2 == "t2"
    assert question_q.theme3 == "t3"

def test_answerUser(answerUser, question_q, user_A):
    assert answerUser.correct == True
    assert answerUser.question.get(pk=question_q.id) == question_q
    assert answerUser.user.get(pk=user_A.id) == user_A

def test_statisc(stats_s, quiz_q):
    assert stats_s.quiz == quiz_q
    assert stats_s.number_participants == 10
    assert stats_s.mean == 15
    assert stats_s.easy == 5
    assert stats_s.medium == 5
    assert stats_s.difficult == 5

def test_grade(grade_g, stats_s):
    assert grade_g.grade == 5
    assert grade_g.number == 10
    assert grade_g.statistics == stats_s

def test_questionScore(stats_s, question_q, questionScore_qs):
    assert questionScore_qs.question == question_q
    assert questionScore_qs.statistics == stats_s
    assert questionScore_qs.score == 5

def test_themeScore(themeScore_ts, stats_s, quiz_q):
    assert themeScore_ts.theme == "t1"
    assert themeScore_ts.score == 5
    assert themeScore_ts.statistics == stats_s
    assert themeScore_ts.quiz == quiz_q