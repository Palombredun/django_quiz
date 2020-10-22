from django.shortcuts import render

from quiz.models import Quiz


def home(request):
    """
    Home page of the website.
    """
    quiz_list = Quiz.objects.order_by("-created")[:5]
    return render(request, "core/home.html", {"quiz_list": quiz_list})


def handler404(request, exception):
    """
    Custom page 404
    """
    data = {}
    return render(request, "core/404.html", data)


def handler500(request):
    """
    Custome page 500
    """
    data = {}
    return render(request, "core/500.html", data)
