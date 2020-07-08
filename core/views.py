from random import randint

from django.shortcuts import render


def home(request):
    return render(request, "core/home.html")


def handler404(request, exception):
    data = {}
    return render(request, "core/404.html", data)


def handler500(request):
    data = {}
    return render(request, "core/500.html", data)
