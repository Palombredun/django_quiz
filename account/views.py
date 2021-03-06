from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import UserRegistrationForm
from quiz.models import Quiz

import logging

logger = logging.getLogger(__name__)

def register(request):
    """
    Creation of the user account.
    It requires a username, an email adress and a password.    
    """
    logger.info("{levelname} {asctime} - A user landed on the register page")
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            logger.info("{levelname} {asctime} - User sent a valid form")
            #  Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data["password"])
            # Save the User object
            new_user.save()
            return redirect('login')
    else:
        logger.warning("{levelname} {asctime} - User did not send a valid registration form")
        user_form = UserRegistrationForm()
    return render(request, "account/register.html", {"form": user_form})
