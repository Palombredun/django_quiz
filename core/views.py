from django.shortcuts import render
from django.forms import formset_factory

from quiz.models import SubCategory

from quiz.forms import QuizForm
from true_false.forms import TrueFalseForm
from multichoice.forms import MultiChoiceForm


def home(request):
    return render(request, "core/home.html")


def create(request):
    TF_Formset = formset_factory(TrueFalseForm)
    MC_Formset = formset_factory(MultiChoiceForm)
    if request.method == "GET":
        quiz_title = QuizForm(request.GET or None, prefix="title")
        tf_formset = TF_Formset(request.GET or None, prefix="tf")
        mc_formset = MC_Formset(request.GET or None, prefix="mc")
    elif request.method == "POST":
        quiz_title = QuizForm(request.POST, prefix="title")
        tf_formset = TF_Formset(request.POST, prefix="tf")
        mc_formset = MC_Formset(request.POST, prefix="mc")
        if tf_formset.is_valid() and mc_formset.is_valid() and quiz_title.is_valid():
            for form in tf_formset:
                cd = form.cleaned_data
                print(cd)
                print(cd["content"])
    return render(
        request,
        "core/create.html",
        {"title_form": quiz_title, "tf_form": tf_formset, "mc_form": mc_formset},
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
