from django import forms

from .models import TF_Question

class TF_Quiz_Form(forms.Form):
	category = forms.CharField()
	sub_category = forms.CharField()
	question = forms.CharField()
	correct = forms.BooleanField()
	order = forms.IntegerField()

	class Meta:
		model = TF_Question