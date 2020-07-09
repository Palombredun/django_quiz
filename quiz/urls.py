from django.urls import path

from . import views
from quiz.views import QuizListView

urlpatterns = [
    path("tutorial/", views.tutorial, name="tutorial"),
    path("create/", views.create, name="create"),
    path(
        "ajax/load-subcategories",
        views.load_sub_categories,
        name="ajax_load_subcategories",
    ),
    path("take-quiz/<slug:url>/", views.take_quiz, name="take_quiz"),
    path("quiz-list/", QuizListView.as_view(), name="quiz-list"),
]
