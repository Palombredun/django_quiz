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
        (2, "Français"),
        (3, "Langues"),
        (4, "Histoire Géographie"),
        (5, "Autres"),
    )
    SUBCATEGORY_CHOICES = (
        (None, ""),
        (1, "Physique"),
        (2, "Chimie"),
        (3, "Sciences de la Vie et de la Terre"),
        (4, "Biologie"),
        (5, "Informatique"),
        (6, "Technologie"),
        (7, "Sciences de l'Ingénieur"),
        (8, "Mathématiques"),
        (9, "Autres"),
        (10, "Orthographe"),
        (11, "Grammaire"),
        (12, "Vocabulaire"),
        (13, "Littérature"),
        (14, "Autres"),
        (15, "Anglais"),
        (16, "Italien"),
        (17, "Espagnol"),
        (18, "Allemand"),
        (19, "Portugais"),
        (20, "Autres"),
        (21, "Histoire"),
        (22, "Géographie"),
        (23, "Enseignement Moral et Civique"),
        (24, "Sciences Economiques et Sociales"),
        (25, "Autres"),
    )
    title = forms.CharField(max_length=100, label="Titre")
    description = forms.CharField(max_length=1000, widget=forms.Textarea)
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, label="Catégorie")
    sub_category = forms.ChoiceField(
        choices=SUBCATEGORY_CHOICES, required=False, label="Sous-catégorie"
    )
    random_order = forms.BooleanField(required=False, label="Ordre aléatoire ?")
