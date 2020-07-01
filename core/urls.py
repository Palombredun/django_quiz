from django.urls import path

from . import views

urlpatterns = [
    path("", views.create, name="home"),
    path("ajax/load-subcategories", views.load_sub_categories, name="ajax_load_subcategories"),
]

