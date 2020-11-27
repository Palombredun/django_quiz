from collections import defaultdict

from .models import Statistic

class Statistics:
	"""
	Class dedicated to the creation of the statistics used for
	the page of the same name.
	"""
	def __init__(self):
		self.difficulty = {1: 0, 2: 0, 3: 0}
		self.themes = defaultdict(int)
		self.participants = 0
		self.good_answers = 0

	def statistics_tf(self, tf_answers):
		for qid, answer in tf_answers.items():
			self.participants += 1
            question = TF_Question.objects.get(id=qid)

            if answer == str(question.correct):
            	self.good_answers += 1
            	self.difficulty[question.difficulty] += 1
            	self.themes[question.]





pour chaque quiz:
	augmenter nb participants
pour chaque question du quiz:
	si correcte:
		incrémenter valeurs question_réussie, diff, theme
update valeurs globales : moyenne, note