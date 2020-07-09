from django.shortcuts import render, redirect
from django.forms import formset_factory
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required

from quiz.forms import QuizForm
from true_false.forms import TrueFalseForm
from multichoice.forms import MultiChoiceForm

from quiz.models import Quiz, SubCategory
from true_false.models import TF_Question
from multichoice.models import MCQuestion


def tutorial(request):
    return render(request, "quiz/tutorial.html")


@login_required
def create(request):
    """
    View dedicated to the creation of the quiz using formsets.
    If the user has never created a quiz, redirect him to the tutorial.
    """
    TF_Formset = formset_factory(TrueFalseForm)
    MC_Formset = formset_factory(MultiChoiceForm)
    if request.method == "GET":
        # if Quiz.objects.filter(creator=request.user).exists():
        quiz_form = QuizForm(request.GET or None, prefix="title")
        tf_formset = TF_Formset(request.GET or None, prefix="tf")
        mc_formset = MC_Formset(request.GET or None, prefix="mc")
        # else:
        #    pass
        #    #return redirect("tutorial")

    elif request.method == "POST":
        quiz_form = QuizForm(request.POST, prefix="title")
        tf_formset = TF_Formset(request.POST, prefix="tf")
        mc_formset = MC_Formset(request.POST, prefix="mc")

        if quiz_form.is_valid() and tf_formset.is_valid() and mc_formset.is_valid():
            try:
                last_quiz = Quiz.objects.latest("created")
                last_id = last_quiz.id
            except Quiz.DoesNotExist:
                last_id = 1

            quiz_cd = quiz_form.cleaned_data
            new_quiz = Quiz(
                title=quiz_cd["title"],
                description=quiz_cd["description"],
                creator=request.user,
                url=slugify(quiz_cd["title"]) + "-" + str(last_id + 1),
                category=quiz_cd["category"],
                sub_category=quiz_cd["sub_category"],
                random_order=quiz_cd["random_order"],
            )
            new_quiz.save()

            mean_difficulty = 0
            n = 0

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

            if mean_difficulty < 1.667:
                quiz_difficulty = 1
            elif mean_difficulty > 2.333:
                quiz_difficulty = 3
            else:
                quiz_difficulty = 2
            new_quiz.difficulty = quiz_difficulty
            new_quiz.save()

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
        request,
        "core/sub_categories_dropdown_list.html",
        {"sub_categories": sub_categories},
    )
