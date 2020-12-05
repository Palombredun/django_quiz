from collections import defaultdict
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
    ThemeScore,
)
from quiz.results import Score, Total, Result
from true_false.models import TF_Question
from multichoice.models import MCQuestion

import pytest


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
        difficulty=1,
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
def truefalse_tf(db, quiz_q):
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
def multichoice_mc(db, quiz_q):
    return MCQuestion.objects.create(
        quiz=quiz_q,
        difficulty=1,
        order=1,
        figure=None,
        content="question",
        explanation=None,
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
def answerUser_au(db, question_q, user_A):
    a = AnswerUser.objects.create(correct=True)
    a.save()
    a.question.add(question_q)
    a.user.add(user_A)
    return a


@pytest.fixture
def stats_s(db, quiz_q):
    return Statistic.objects.create(
        quiz=quiz_q, number_participants=10, mean=15, easy=5, medium=5, difficult=5
    )


@pytest.fixture
def grade_g(db, stats_s):
    return Grade.objects.create(grade=5, number=10, statistics=stats_s)


@pytest.fixture
def questionScore_qs(db, stats_s, question_q):
    return QuestionScore.objects.create(
        question=question_q, statistics=stats_s, score=5
    )


@pytest.fixture
def themeScore_ts(db, stats_s, quiz_q):
    return ThemeScore.objects.create(
        theme="t1", score=5, statistics=stats_s, quiz=quiz_q
    )


@pytest.fixture
def score_s():
    return Score()


@pytest.fixture
def total_t():
    return Total(1)


@pytest.fixture
def result_r():
    return Result()


@pytest.fixture
def question_true(db, quiz_q):
    return TF_Question.objects.create(
        quiz=quiz_q,
        difficulty=0,
        order=0,
        figure=None,
        content="true",
        explanation=None,
        theme1="",
        theme2="",
        theme3="",
        correct=True,
    )


@pytest.fixture
def question_false(db, quiz_q):
    return TF_Question.objects.create(
        quiz=quiz_q,
        difficulty=0,
        order=0,
        figure=None,
        content="true",
        explanation=None,
        theme1="",
        theme2="",
        theme3="",
        correct=False,
    )


### Test Score ###
def test_init_score(score_s):
    assert score_s.nb_good_answers == 0
    assert score_s.weighted == 0
    assert score_s.difficulty == {1: 0, 2: 0, 3: 0}
    assert score_s.theme == defaultdict(int)
    assert score_s.questions == []


def test_score_add_correct_question(question_q, score_s):
    score_s.add_correct_question(question_q)

    assert score_s.nb_good_answers == 1
    assert score_s.weighted == 1
    assert score_s.difficulty == {1: 1, 2: 0, 3: 0}
    assert score_s.theme == {"t1": 1, "t2": 1, "t3": 1}
    assert score_s.questions == [question_q]


### Test Total ###
def test_init_total(total_t):
    assert total_t.weighted == 0
    assert total_t.difficulty == {1: 0, 2: 0, 3: 0}
    assert total_t.theme == defaultdict(int)
    assert total_t.nb_questions == 1


def test_populate_total_t(total_t, question_q):
    total_t.populate(question_q)

    assert total_t.weighted == 1
    assert total_t.difficulty == {1: 1, 2: 0, 3: 0}
    assert total_t.theme == {"t1": 1, "t2": 1, "t3": 1}


### Test Result ###
def test_init_result(result_r):
    assert result_r.details == {}
    assert result_r.advices == {}


def test_is_tf_answer_correct(result_r, question_true):
    """
    GIVEN a correct answer to a question
    WHEN Result._is_tf_answer_correct is called
    THEN assert it returns True
    """
    result = "True"
    question = question_true

    res = result_r._is_tf_answer_correct(result, question_true)

    assert res is True


def test_is_tf_answer_incorrect(result_r, truefalse_tf, question_false):
    """
    GIVEN an incorrect answer to a question
    WHEN Result._is_tf_answer_correct is called
    THEN assert it returns False
    """
    result = "False"
    question = question_false

    res = result_r._is_tf_answer_correct(result, question)

    assert res is False


def test_create_answerUser(db, result_r, question_q, user_A):
    """
    GIVEN an answer to a question not answered
    WHEN the method Result._update_or_create_answerUser
    THEN assert a new entry has been created
    """
    question = question_q
    user = user_A
    correct = True

    answer_user = result_r._update_or_create_answerUser(question, user, correct)

    users = answer_user.user.all()
    questions = answer_user.question.all()
    assert user_A in users
    assert len(users) == 1
    assert question_q in questions
    assert len(questions) == 1
    assert answer_user.correct == True


def test_update_answerUser(answerUser_au, result_r, question_q, user_A):
    """
    GIVEN an answer to a question already answered
    WHEN the method Result._update_or_create_answerUser
    THEN assert the field 'correct' has been correctly updated
    """
    question = question_q
    user = user_A
    correct = False

    answer_user = result_r._update_or_create_answerUser(question, user, correct)

    users = answer_user.user.all()
    questions = answer_user.question.all()
    assert user_A in users
    assert len(users) == 1
    assert question_q in questions
    assert len(questions) == 1
    assert answer_user.correct == False


def test_update_details_tf_with_true(result_r, question_q):
    """
    GIVEN a result True and a tf question whose good answer is True
    WHEN Result._update_details_tf is called
    THEN assert Result.details is updated with a string indicating the user answered well
    """
    result = True
    question = question_q

    details = result_r._update_details_tf(result, question)

    assert details["question"] == "Vous avez bien répondu"



def test_update_details_tf_with_false_question_correct(result_r, question_q):
    """
    GIVEN a result False and a tf question whose good answer is True
    WHEN Result._update_details_tf is called
    THEN assert Result.details is updated with a string indicating the good answer is True
    """
    result = False
    question = question_q

    details = result_r._update_details_tf(result, question)

    assert details["question"] == "La bonne réponse était Vrai"


def test_update_details_tf_with_false_question_incorrect(result_r, question_q):
    """
    GIVEN a result False and a tf question whose good answer is False
    WHEN Result._update_details_tf is called
    THEN assert Result.details is updated with a string indicating the good answer is False
    """
    result = False
    question = question_q
    good_answer = False

    details = result_r._update_details_tf(result, question, question_correct=good_answer)

    assert details["question"] == "La bonne réponse était Faux"


def test_update_details_mc_with_true(result_r, multichoice_mc):
    """
    GIVEN a result True and a multichoice question
    WHEN Result._update_details_mc
    THEN assert Result.details has been updated with a message the question is passed
    """
    result = True
    question = multichoice_mc

    details = result_r._update_details_mc(result, question)

    assert details["question"] == "Vous avez bien répondu"


def test_udate_details_mc_with_false_question(result_r, multichoice_mc):
    """
    GIVEN a result False and a multichoice question
    WHEN Result._update_details_mc
    THEN assert Result.details has been updated with a message indicating the good answer
    """
    result = False
    question = multichoice_mc

    details = result_r._update_details_mc(result, question)

    assert details["question"] == "La bonne réponse était : \na1\n"


def test_compute_global_score_low(result_r):
    """
    GIVEN two ints representing the weighted score of the quiz
    WHEN Result._compute_global_score is called
    THEN assert Result.advices is updated with the appropriate string
    """
    score = 2
    total = 9

    result_r._compute_global_score(score, total)

    assert (
        result_r.advices["global"] == "Vous avez besoin de plus de révisions, courage !"
    )


def test_compute_global_score_medium(result_r):
    """
    GIVEN two ints representing the weighted score of the quiz
    WHEN Result._compute_global_score is called
    THEN assert Result.advices is updated with the appropriate string
    """
    score = 5
    total = 9

    result_r._compute_global_score(score, total)

    assert (
        result_r.advices["global"]
        == "Avec un peu de travail supplémentaire, vous réussirez !"
    )


def test_compute_global_score_high(result_r):
    """
    GIVEN two ints representing the weighted score of the quiz
    WHEN Result._compute_global_score is called
    THEN assert Result.advices is updated with the appropriate string
    """
    score = 9
    total = 9

    result_r._compute_global_score(score, total)

    assert result_r.advices["global"] == "Vous avez très bien réussi le quiz !"


def test_compute_nb_good_answers(result_r):
    """
    GIVEN two int representing the number of well answered questions of a quiz
    WHEN Result._compute_nb_good_answers is called
    THEN assert Result.advices has been updated with the corresponding new entry
    """
    score = 0
    total = 10

    result_r._compute_nb_good_answers(score, total)

    assert (
        result_r.advices["good_answers"]
        == "Vous avez bien répondu à 0 questions sur 10"
    )


def test_compute_difficulty_successful(result_r):
    """
    GIVEN two valid dicts representing a successful quiz
    WHEN the method _compute_difficulty is called
    THEN Result.advices must be updated with a corresponding new entry
    """
    score = {1: 5, 2: 3, 3: 2}
    total = {1: 5, 2: 3, 3: 2}
    result_r._compute_difficulty(score, total)
    assert (
        result_r.advices["difficulty"]
        == "Vous maîtrisez très bien ce sujet, félicitations !"
    )


def test_compute_difficulty_0_difficult(result_r):
    """
    GIVEN two valid dicts representing a quiz where difficults question are failed
    WHEN the method _compute_difficulty is called
    THEN Result.advices must be update with a corresponding new entry
    """
    score = {1: 5, 2: 3, 3: 0}
    total = {1: 5, 2: 3, 3: 2}

    result_r._compute_difficulty(score, total)
    
    assert (
        result_r.advices["difficulty"]
        == "Vous maîtrisez bien ce sujet sujet mais les questions plus avancées vous échappent encore"
    )


def test_compute_difficilty_0_medium(result_r):
    """
    GIVEN two valid dicts representing a quiz where medium and difficults questions are failed
    WHEN the method _compute_difficulty is called
    THEN Result.advices must be update with a corresponding new entry
    """
    score = {1: 5, 2: 0, 3: 0}
    total = {1: 5, 2: 3, 3: 2}

    result_r._compute_difficulty(score, total)

    assert (
        result_r.advices["difficulty"]
        == "Vous semblez maîtriser les bases, poursuivez vos efforts !"
    )


def test_compute_difficulty_0_easy(result_r):
    """
    GIVEN two valid dicts representing a quiz where all questions are failed
    WHEN the method _compute_difficulty is called
    THEN Result.advices must be update with a corresponding new entry
    """
    score = {1: 0, 2: 0, 3: 0}
    total = {1: 5, 2: 3, 3: 2}

    result_r._compute_difficulty(score, total)

    assert (
        result_r.advices["difficulty"]
        == "Vous ne semblez pas maîtriser le sujet. Commencez par revoir les bases."
    )


def test_compute_difficulty_no_logic(result_r):
    """
    GIVEN two valid dicts representing a quiz where easy and difficult are successful but not medium ones
    WHEN the method _compute_difficulty is called
    THEN Result.advices must NOT be update with a corresponding new entry
    """
    score = {1: 5, 2: 0, 3: 2}
    total = {1: 5, 2: 3, 3: 2}

    result_r._compute_difficulty(score, total)

    assert "difficulty" not in result_r.advices.keys()


def test_compute_theme_successful(result_r):
    """
    GIVEN two dicts representing the theme scores
    THEN the method _compute_theme is called
    THEN Result.advices must be updated N (number of themes) entries
    """
    themes = {"définition": 2, "cours": 3, "exercice": 4}
    total = {"définition": 2, "cours": 3, "exercice": 4}

    result_r._compute_theme(themes, total)

    assert (
        result_r.advices["définition"]
        == "Vous avez bien réussi les questions sur le thème : définition"
    )
    assert (
        result_r.advices["cours"]
        == "Vous avez bien réussi les questions sur le thème : cours"
    )
    assert (
        result_r.advices["exercice"]
        == "Vous avez bien réussi les questions sur le thème : exercice"
    )


def test_compute_theme_failed(result_r):
    """
    GIVEN two dicts representing the theme scores
    THEN the method _compute_theme is called
    THEN Result.advices must be updated N (number of themes) entries
    """
    themes = {"définition": 0, "cours": 0, "exercice": 0}
    total = {"définition": 2, "cours": 3, "exercice": 4}

    result_r._compute_theme(themes, total)

    assert (
        result_r.advices["définition"]
        == "Vous devriez réviser le sujet suivant : définition"
    )
    assert result_r.advices["cours"] == "Vous devriez réviser le sujet suivant : cours"
    assert (
        result_r.advices["exercice"]
        == "Vous devriez réviser le sujet suivant : exercice"
    )
