from django.shortcuts import render
from django.forms import formset_factory

from true_false.forms import TrueFalseForm, TF_Formset
from multichoice.forms import MultiChoiceForm, MC_Formset

def home(request):
    return render(request, 'core/home.html')


def create(request):
    if request.method == "GET":
        tf_formset = TF_Formset(request.GET or None)
        mc_formset = MC_Formset(request.GET or None)
    elif request.method == "POST":
            tf_formset = TF_Formset(request.POST)
            mc_formset = MC_Formset(request.POST)
    return render(request, "core/create.html", {"tf_form": tf_formset, "mc_form": mc_formset})
