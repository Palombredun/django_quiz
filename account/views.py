from django.shortcuts import render
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView


from .forms import UserRegistrationForm


def register(request):
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

class MyLoginView(SuccessMessageMixin ,LoginView):
    template_name = 'registration/login.html'
    success_url = 'home'
    success_message = 'Vous êtes bien connecté'

class MyLogoutView(SuccessMessageMixin, LogoutView):
    template_name = "registration/logged_out.html"
    success_url = "home"
    success_message = "Vous avez bien été déconnecté"