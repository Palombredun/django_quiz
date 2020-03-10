from django.shortcuts import render
from django.forms import formset_factory

from true_false.forms import TrueFalseForm
from multichoice.forms import MultiChoiceForm

def home_page_view(request):
    TF_formset = formset_factory(TrueFalseForm)
    MC_formset = formset_factory(MultiChoiceForm)
    
    if request.method == "POST":
        tf_formset = TF_formset(request.POST or None)
        mc_formset = MC_formset(request.POST or None)
        
    
    tf_form = TF_formset()
    mc_form = MC_formset()

    return render(request, 'core/home.html', 
        {'tf_form': tf_form, 'mc_form': mc_form})