from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.create, name="create"),
    path(
        "ajax/load-subcategories",
        views.load_sub_categories,
        name="ajax_load_subcategories",
    ),
    path("tutorial/", views.tutorial, name="tutorial"),
    path("quiz-list/", views.quiz_list, name="quiz-list"),
    path(
        "category/<str:category_name>/",
        views.quiz_list_by_category,
        name="quiz_category_list_matching",
    ),
    path(
        "subcategory/<str:subcategory_name>/",
        views.quiz_list_by_subcategory,
        name="quiz_subcategory_list_matching",
    ),
    path("take/<slug:url>/", views.take, name="take-quiz"),
    path("statistics/<slug:url>", views.statistics, name="statistics"),
]
