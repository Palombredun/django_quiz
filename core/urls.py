from django.urls import path

from . import views

urlpatterns = [
	path("", views.home, name="home"),
	path("license/", views.license, name="license"),
	path("contact/", views.contact, name="contact"),
]