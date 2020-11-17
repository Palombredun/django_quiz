from collections import defaultdict
from random import shuffle

from django.shortcuts import render, redirect, get_object_or_404
from django.forms import formset_factory
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView

from quiz.forms import QuizForm
from true_false.forms import CreationTrueFalseForm, TrueFalseForm
from multichoice.forms import CreationMultiChoiceForm, MultiChoiceForm

from quiz.models import Quiz, Question, Category, SubCategory
from true_false.models import TF_Question
from multichoice.models import MCQuestion

from quiz.results import Result, Score, Total


def tutorial(request):
    response = render(request, "quiz/tutorial.html")
    response.set_cookie("tutorial", "True")
    return response


@login_required
def create(request):
    """
    View dedicated to the creation of the quiz using formsets.
    If the user has never created a quiz, redirect him to the tutorial.
    """
    cookie = request.COOKIES.get("tutorial", "False")
    if (
        Quiz.objects.filter(creator=request.user).exists() == False
        and cookie == "False"
    ):
        response = redirect("tutorial")
        response.set_cookie("tutorial", "True", 1800)
        return response

    TF_Formset = formset_factory(CreationTrueFalseForm)
    MC_Formset = formset_factory(CreationMultiChoiceForm)
    if request.method == "GET":
        quiz_form = QuizForm(request.GET or None, prefix="quiz")
        tf_formset = TF_Formset(request.GET or None, prefix="tf")
        mc_formset = MC_Formset(request.GET or None, prefix="mc")
    elif request.method == "POST":
        quiz_form = QuizForm(request.POST, prefix="quiz")
        tf_formset = TF_Formset(request.POST or None, prefix="tf")
        mc_formset = MC_Formset(request.POST or None, prefix="mc")

        if quiz_form.is_valid() and ((tf_formset.is_valid() and mc_formset.is_valid())):
            quiz_cd = quiz_form.cleaned_data

            category = Category.objects.get(id=quiz_cd["category"])
            category_name = (
                category.category.replace(" ", "-").replace("ç", "c").replace("é", "e")
            )
            if quiz_cd["sub_category"]:
                sub_category = SubCategory.objects.get(id=quiz_cd["sub_category"])
            else:
                sub_category = None
            new_quiz = Quiz(
                title=quiz_cd["title"],
                description=quiz_cd["description"],
                creator=request.user,
                url="placeholder",
                category=category,
                category_name=category_name,
                sub_category=sub_category,
                random_order=quiz_cd["random_order"],
                difficulty=0,
            )
            new_quiz.save()

            mean_difficulty = 0
            n = 0

            if tf_formset:
                for question in tf_formset:
                    cd = question.cleaned_data
                    n += 1
                    mean_difficulty += int(cd["difficulty"])
                    new_tf = TF_Question(
                        content=cd["content"],
                        difficulty=cd["difficulty"],
                        theme1=cd["theme1"],
                        theme2=cd["theme2"],
                        theme3=cd["theme3"],
                        order=cd["order"],
                        correct=cd["correct"],
                        quiz=new_quiz,
                    )
                    new_tf.save()

            if mc_formset:
                for question in mc_formset:
                    cd = question.cleaned_data
                    n += 1
                    mean_difficulty += int(cd["difficulty"])
                    new_mc = MCQuestion(
                        content=cd["content"],
                        difficulty=cd["difficulty"],
                        theme1=cd["theme1"],
                        theme2=cd["theme2"],
                        theme3=cd["theme3"],
                        order=cd["order"],
                        answer1=cd["answer1"],
                        answer2=cd["answer2"],
                        answer3=cd["answer3"],
                        answer1_correct=cd["answer1_correct"],
                        answer2_correct=cd["answer2_correct"],
                        answer3_correct=cd["answer3_correct"],
                        quiz=new_quiz,
                    )
                    new_mc.save()
            mean_difficulty /= n
            # the difficulty is
            if mean_difficulty < 1.667:
                quiz_difficulty = 1
            elif mean_difficulty > 2.333:
                quiz_difficulty = 3
            else:
                quiz_difficulty = 2
            new_quiz.difficulty = quiz_difficulty
            new_quiz.url = slugify(quiz_cd["title"]) + "-" + str(new_quiz.id)
            new_quiz.save()

            return redirect("profile")

    return render(
        request,
        "quiz/create.html",
        {"quiz_form": quiz_form, "tf_form": tf_formset, "mc_form": mc_formset},
    )


def load_sub_categories(request):
    category_id = request.GET.get("category")
    sub_categories = SubCategory.objects.filter(category_id=category_id).order_by(
        "sub_category"
    )
    return render(
        request, "quiz/subcategories_dropdown.html", {"sub_categories": sub_categories}
    )


def quiz_list(request):
    quiz_list = Quiz.objects.all().order_by("-created")
    categories = Category.objects.all()
    return render(
        request,
        "quiz/quiz_list.html",
        {"quiz_list": quiz_list, "categories": categories},
    )


def quiz_list_by_category(request, category_name):
    category = Category.objects.get(category=category_name)
    subcategories = SubCategory.objects.filter(category=category)
    quiz = Quiz.objects.filter(category=category)
    return render(
        request,
        "quiz/view_quiz_category.html",
        {"category": category_name, "subcategories": subcategories, "quiz_list": quiz},
    )


def quiz_list_by_subcategory(request, subcategory_name):
    subcategory_id = SubCategory.objects.get(sub_category=subcategory_name)
    quiz = Quiz.objects.filter(sub_category=subcategory_id)
    return render(
        request,
        "quiz/view_quiz_subcategory.html",
        {"subcategories": subcategory_name, "quiz_list": quiz},
    )

@login_required
def take(request, url):
    """
    Send questions belonging to the quiz
    Receive results, compare them to the answers,
    redirect to page results
    """

    quiz = get_object_or_404(Quiz, url=url)
    tf_questions = TF_Question.objects.filter(quiz=quiz).order_by("order")
    mc_questions = MCQuestion.objects.filter(quiz=quiz).order_by("order")

    nb_tf_questions = tf_questions.count()
    nb_mc_questions = mc_questions.count()
    forms = [0] * (nb_tf_questions + nb_mc_questions)
    id_questions = [0] * (nb_tf_questions + nb_mc_questions)

    for question in tf_questions:
        index = question.order
        forms[index] = (
            "tf",
            question.content,
            TrueFalseForm(
                request.GET or None,
                initial={"qid": question.id},
                prefix="tf" + str(index),
            ),
        )
        id_questions[index] = question.id
    for question in mc_questions:
        index = question.order
        forms[index] = (
            "mc",
            question.content,
            question.answer1,
            question.answer2,
            question.answer3,
            MultiChoiceForm(
                request.GET or None,
                initial={"qid": question.id},
                prefix="mc" + str(index),
            ),
        )

    if request.method == "GET":
        if quiz.random_order is True:
            shuffle(forms)
        return render(request, "quiz/take.html", {"title": quiz.title, "description": quiz.description, "forms": forms})

    elif request.method == "POST":
        tf_answers = {}
        for i in range(nb_tf_questions):
            tf = TrueFalseForm(request.POST or None, prefix="tf" + str(i))
            if tf.is_valid():
                cd = tf.cleaned_data
                tf_answers[cd["qid"]] = cd["correct"]
        mc_answers = {}
        for i in range(nb_mc_questions):
            mc = MultiChoiceForm(request.POST or None, prefix="mc" + str(i))
            if mc.is_valid():
                cd = mc.cleaned_data
                mc_answers[cd["qid"]] = (cd["answer1"], cd["answer2"], cd["answer3"])
        total_questions = nb_tf_questions + nb_mc_questions

        score_user = Score()
        total_score = Total(total_questions)
        results = Result()

        results.statistics_tf(tf_answers, score_user, total_score)
        results.statistics_mc(mc_answers, score_user, total_score)
        results.compute_scores(score_user, total_score)

        return render(
            request,
            "quiz/results.html",
            {"details": results.details, "advices": results.advices},
        )
