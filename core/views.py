from django.shortcuts import render
from django.forms import modelformset_factory

from true_false.forms import TFQuizForm

def home_page_view(request):
	form = TFQuizForm()
	return render(request, 'core/home.html', {'form': form})