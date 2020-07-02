from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.create, name="create"),
    path("ajax/load-subcategories", views.load_sub_categories, name="ajax_load_subcategories"),
]