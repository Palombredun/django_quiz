from django.shortcuts import render
from django.forms import formset_factory

from true_false.forms import TF_Quiz_Form

def home_page_view(request):
	TF_Quiz_FormSet = formset_factory(TF_Quiz_Form)
	form = TF_Quiz_FormSet()
	return render(request, 'core/home.html', {'form': form})