from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from quiz.models import Quiz, AnswerUser

# Create your views here.
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
        data["quiz_participated"] = []
        for qid in questions_id:
            quiz_participated = Quiz.objects.filter(question=qid)[0]
            data["quiz_participated"].append(quiz_participated)
        data["quiz_participated"] = set(data["quiz_participated"])
    if quiz_created:
        data["quiz_created"] = quiz_created
    data["user"] = user

    return render(
        request,
        "profiles/profile.html",
        data,
    )