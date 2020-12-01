from django.shortcuts import render
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import UserRegistrationForm
from quiz.models import Quiz


def register(request):
    """
    Creation of the user account.
    It requires a username, an email adress and a password.    
    """
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            #  Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data["password"])
            # Save the User object
            new_user.save()
            # messages.success(request, "Compte crée")
            return render(request, "core/home.html", {"new_user": new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, "account/register.html", {"form": user_form})


@login_required
def profile(request):
    """
    Profile page of the user
    It displays the quiz he or she has passed and the quiz 
    he or she has created.
    """
    user = User.objects.get(pk=request.user.id)
    quiz_created = Quiz.objects.filter(creator=user).order_by("-created")
    questions_participated = AnswerUser.objects.filter(user=user)
    
    data = {}
    if questions_participated:
        questions_id = [question.id for question in questions_participated]
        quiz_participated = set(Quiz.objects.filter(question=questions_id))
        data["quiz_participated"] = quiz_participated
    if quiz_created:
        data["quiz_created"] = quiz_created
    data["user"] = user

    return render(
        request,
        "account/profile.html",
        data,
    )
