from django.urls import path

from . import views
from quiz.views import QuizListView, CategoryListView

urlpatterns = [
    path("create/", views.create, name="create"),
    path(
        "ajax/load-subcategories",
        views.load_sub_categories,
        name="ajax_load_subcategories",
    ),
    path("tutorial/", views.tutorial, name="tutorial"),
    path("take/<slug:url>/", views.take_quiz, name="take"),
    path("quiz-list/", QuizListView.as_view(), name="quiz-list"),
    path("category-list/", CategoryListView.as_view(), name="category-list"),
    path(
        "<str:category_name>",
        views.quiz_list_by_category,
        name="quiz_category_list_matching",
    ),
]
