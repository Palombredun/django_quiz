from django.shortcuts import render
from django.forms import formset_factory

from true_false.forms import TrueFalseForm, TF_Formset
from multichoice.forms import MultiChoiceForm, MC_Formset

# def home_page_view(request):
#    TF_formset = formset_factory(TrueFalseForm, extra=1)
#    MC_formset = formset_factory(MultiChoiceForm)
#
#    if request.method == "POST":
#        tf_formset = TF_formset(request.POST or None)
#        for tf in tf_formset:
#           print(tf)
#        #mc_formset = MC_formset(request.POST or None)
#
#    tf_form = TF_formset()
#    #mc_form = MC_formset()
#    return render(request, "core/home.html", {'tf_form': tf_form})
#    #return render(request, 'core/home.html',
#    #    {'tf_form': tf_form, 'mc_form': mc_form})


def home_page_view(request):
    if request.method == "GET":
        tf_formset = TF_Formset(request.GET or None, prefix="tf_form")
        mc_formset = MC_Formset(request.GET or None, prefix="mc_form")
    elif request.method == "POST":
        if "tf_form" in request.POST:
            tf_formset = TF_Formset(request.POST, prefix="tf_form")
        if "mc_form" in request.POST:
            mc_formset = MC_Formset(request.POST, prefix="mc_form")
    return render(request, "core/home.html", {"tf_form": tf_formset, "mc_form": mc_formset})
