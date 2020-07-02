from random import randint

from django.shortcuts import render
from django.forms import formset_factory
from django.utils.text import slugify

from quiz.models import SubCategory

from quiz.forms import QuizForm
from true_false.forms import TrueFalseForm
from multichoice.forms import MultiChoiceForm

from quiz.models import Quiz

def create(request):
    TF_Formset = formset_factory(TrueFalseForm)
    MC_Formset = formset_factory(MultiChoiceForm)
    if request.method == "GET":
        quiz_form = QuizForm(request.GET or None, prefix="title")
        tf_formset = TF_Formset(request.GET or None, prefix="tf")
        mc_formset = MC_Formset(request.GET or None, prefix="mc")
    elif request.method == "POST":
        quiz_form = QuizForm(request.POST, prefix="title")
        tf_formset = TF_Formset(request.POST, prefix="tf")
        mc_formset = MC_Formset(request.POST, prefix="mc")
        
        if quiz_form.is_valid() and tf_formset.is_valid() and mc_formset.is_valid():
            quiz_cd = quiz_form.cleaned_data
            new_quiz = Quiz.objects.create(title=quiz_cd["title"],
                            description=quiz_cd["description"],
                            creator=request.user,
                            url=slugify(quiz_cd["title"]) + '-' + str(randint(0,999)),
                            category=quiz_cd["category"],
                            sub_category=quiz_cd["sub_category"],
                            random_order=quiz_cd["random_order"]
                            )
        
        difficulty = 0
        nb_of_questions = 0
        if tf_formset.is_valid():
            for question in tf_formset:
                cd = question.cleaned_data
                difficulty += cd["difficulty"]
                nb_of_questions += 1
        mean_difficulty = difficulty/nb_of_questions
        if mean_difficulty < 1.667:
            quiz_difficulty = 1
        elif mean_difficulty > 2.333:
            quiz_difficulty = 3
        else:
            quiz_difficulty = 2
    return render(
        request,
        "core/create.html",
        {"title_form": quiz_form, "tf_form": tf_formset, "mc_form": mc_formset},
    )

def load_sub_categories(request):
    category_id = request.GET.get("category")
    sub_categories = SubCategory.objects.filter(category_id=category_id).order_by(
        "sub_category"
    )
    return render(
        request,
        "core/sub_categories_dropdown_list.html",
        {"sub_categories": sub_categories},
    )
