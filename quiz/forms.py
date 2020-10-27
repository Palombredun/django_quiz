from django import forms

from quiz.models import Quiz, Question, Category, SubCategory


DIFFICULTY_CHOICES = ((1, "facile"), (2, "moyen"), (3, "difficile"))


class QuestionForm(forms.Form):
    """
    Base form used for the creation of questions in a quiz.
    """

    content = forms.CharField(max_length=1000, label="Question")
    difficulty = forms.ChoiceField(choices=DIFFICULTY_CHOICES, label="Difficulté")
    theme1 = forms.CharField(
        max_length=100,
        label="Thème 1",
        help_text="Thème de la question",
        required=False,
    )
    theme2 = forms.CharField(
        max_length=100,
        label="Thème 2",
        help_text="Thème de la question",
        required=False,
    )
    theme3 = forms.CharField(
        max_length=100,
        label="Thème 3",
        help_text="Thème de la question",
        required=False,
    )
    order = forms.IntegerField(widget=forms.HiddenInput())


class QuizForm(forms.Form):
    CATEGORY_CHOICES = (
        (None, ""),
        (1, "Sciences"),
        (2, "Langues"),
        (3, "Français"),
        (4, "Autres"),
        (5, "Histoire Géographie"),
    )
    SUBCATEGORY_CHOICES = (
        (None, ""),
        (1, "Physique"),
        (2, "Chimie"),
        (3, "Biologie"),
        (4, "Sciences de la Vie et de la Terre"),
        (5, "Informatique"),
        (6, "Technologie"),
        (7, "Sciences de l'Ingénieur"),
        (8, "Anglais"),
        (9, "Allemand"),
        (10, "Espagnol"),
        (11, "Italien"),
        (12, "Latin"),
        (13, "Orthographe"),
        (14, "Vocabulaire"),
        (15, "Analyse de texte"),
        (16, "Grammaire"),
        (17, "Histoire"),
        (18, "Géographie"),
        (19, "Education Civique et Morale"),
        (20, "Sciences Economiques et Sociales"),
    )
    title = forms.CharField(max_length=100)
    description = forms.CharField(max_length=1000, widget=forms.Textarea)
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)
    sub_category = forms.ChoiceField(choices=SUBCATEGORY_CHOICES, required=False)
    random_order = forms.BooleanField(required=False)