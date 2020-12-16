from django.shortcuts import render

from quiz.models import Quiz

import logging


logger = logging.getLogger(__name__)

def home(request):
    """
    Home page of the website.
    """
    quiz_list = Quiz.objects.order_by("-created")[:5]
    logger.info('{levelname} {asctime} - Request home page')
    return render(request, "core/home.html", {"quiz_list": quiz_list})


def license(request):
    logger.info('{levelname} {asctime} - Request license page')
    return render(request, "core/license.html")


def contact(request):
    logger.info('{levelname} {asctime} - Request contact page')
    return render(request, "core/contact.html")


def handler404(request, exception):
    """
    Custom page 404
    """
    logger.warning(logger.warning('{levelname} {asctime} Page 404 thrown'))
    data = {}
    return render(request, "core/404.html", data)


def handler500(request):
    """
    Custome page 500
    """
    logger.error(logger.error("{levelname} {asctime} {module} {process:d} {thread:d} ERROR 500 !"))
    data = {}
    return render(request, "core/500.html", data)
