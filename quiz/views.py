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
    if (
        Quiz.objects.filter(creator=request.user).exists() == False
        or request.COOKIES.get("tutorial", "False") != "False"
    ):
        # request.COOKIES['tutorial'] = True
        response = render(request, "quiz/tutorial.html")
        response.set_cookie("tutorial", "False")

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
            new_quiz = Quiz(
                title=quiz_cd["title"],
                description=quiz_cd["description"],
                creator=request.user,
                url="placeholder",
                category=quiz_cd["category"],
                sub_category=quiz_cd["sub_category"],
                random_order=quiz_cd["random_order"],
            )
            new_quiz.save()

            mean_difficulty = 0
            n = 0

            if tf_formset:
                for question in tf_formset:
                    cd = question.cleaned_data
                    n += 1
                    mean_difficulty += int(cd["difficulty"]) / n
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
                    mean_difficulty += int(cd["difficulty"]) / n
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

            # the difficulty is
            if mean_difficulty < 1.667:
                quiz_difficulty = 1
            elif mean_difficulty > 2.333:
                quiz_difficulty = 3
            else:
                quiz_difficulty = 2
            new_quiz.difficulty = quiz_difficulty
            new_quiz.slug = slugify(quiz_cd["title"]) + "-" + str(new_quiz.id)
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
    subcategories = SubCategory.objects.all()
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


def take(request, url):
    quiz = get_object_or_404(Quiz, url=url)
    tf_questions = TF_Question.objects.filter(quiz=quiz)
    mc_questions = MCQuestion.objects.filter(quiz=quiz)

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
                initial={"id_question": question.id}, prefix="tf" + str(index)
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
                initial={"id_question": question.id}, prefix="mc" + str(index)
            ),
        )

    if request.method == "GET":
        if quiz.random_order is True:
            shuffle(forms)
        return render(request, "quiz/take.html", {"title": quiz.title, "forms": forms})
    elif request.method == "POST":
        for i in range(nb_tf_questions):
            tf = TrueFalseForm(request.POST, prefix="tf" + str(i))
            if tf.is_valid():
                cd = tf.cleaned_data
        for i in range(nb_tf_questions):
            mc = MultiChoiceForm(request.POST, prefix="mc" + str(i))
            if mc.is_valid():
                cd = mc.cleaned_data
        return render(request, "quiz/results.html")
