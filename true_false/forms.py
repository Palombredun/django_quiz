from django import forms

from .models import TF_Question

class TFQuizForm(forms.Form):

	class Meta:
		model = TF_Question
		fields = '__all__'