from django.shortcuts import render
from django.forms import formset_factory

from true_false.forms import TrueFalseForm, TF_Formset
from multichoice.forms import MultiChoiceForm, MC_Formset

def home_page_view(request):
    return render(request, 'core/home.html')


def create_quiz(request):
    if request.method == "GET":
        tf_formset = TF_Formset(request.GET or None)
        mc_formset = MC_Formset(request.GET or None)
    elif request.method == "POST":
            tf_formset = TF_Formset(request.POST)
            mc_formset = MC_Formset(request.POST)
    return render(request, "core/home.html", {"tf_form": tf_formset, "mc_form": mc_formset})
