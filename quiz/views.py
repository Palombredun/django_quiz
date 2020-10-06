from random import shuffle

from django.shortcuts import render, redirect, get_object_or_404
from django.forms import formset_factory
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView

from quiz.forms import QuizForm
from true_false.forms import CreationTrueFalseForm, TrueFalseForm
from multichoice.forms import CreationMultiChoiceForm, MultiChoiceForm

from quiz.models import Quiz, Question, Category, SubCategory
from true_false.models import TF_Question
from multichoice.models import MCQuestion


def tutorial(request):
    return render(request, "quiz/tutorial.html")


@login_required
def create(request):
    """
    View dedicated to the creation of the quiz using formsets.
    If the user has never created a quiz, redirect him to the tutorial.
    """
    TF_Formset = formset_factory(CreationTrueFalseForm)
    MC_Formset = formset_factory(CreationMultiChoiceForm)
    if request.method == "GET":
        quiz_form = QuizForm(request.GET or None, prefix="quiz")
        tf_formset = TF_Formset(request.GET or None, prefix="tf")
        mc_formset = MC_Formset(request.GET or None, prefix="mc")
    elif request.method == "POST":
        quiz_form = QuizForm(request.POST, prefix="quiz")
        tf_formset = TF_Formset(request.POST or None, prefix="tf")
        mc_formset = MC_Formset(request.POST or None, prefix="mc")

        if quiz_form.is_valid() and (
            (tf_formset and tf_formset.is_valid())
            and (mc_formset and mc_formset.is_valid())
        ):

            quiz_cd = quiz_form.cleaned_data
            new_quiz = Quiz(
                title=quiz_cd["title"],
                description=quiz_cd["description"],
                creator=request.user,
                url=slugify(quiz_cd["title"]),
                category=quiz_cd["category"],
                sub_category=quiz_cd["sub_category"],
                random_order=quiz_cd["random_order"],
            )
            new_quiz.save()

            mean_difficulty = 0
            n = 0
            for question in tf_formset:
                cd = question.cleaned_data
                n += 1
                mean_difficulty += int(cd["difficulty"]) / n
                new_tf = TF_Question(
                    content=cd["content"],
                    difficulty=cd["difficulty"],
                    theme1=cd["theme1"],
                    theme2=cd["theme2"],
                    theme3=cd["theme3"],
                    order=cd["order"],
                    correct=cd["correct"],
                    quiz=new_quiz,
                )
                new_tf.save()
            for question in mc_formset:
                cd = question.cleaned_data
                n += 1
                mean_difficulty += int(cd["difficulty"]) / n
                new_mc = MCQuestion(
                    content=cd["content"],
                    difficulty=cd["difficulty"],
                    theme1=cd["theme1"],
                    theme2=cd["theme2"],
                    theme3=cd["theme3"],
                    order=cd["order"],
                    answer1=cd["answer1"],
                    answer2=cd["answer2"],
                    answer3=cd["answer3"],
                    answer1_correct=cd["answer1_correct"],
                    answer2_correct=cd["answer2_correct"],
                    answer3_correct=cd["answer3_correct"],
                    quiz=new_quiz,
                )
                new_mc.save()

                # the difficulty is
                if mean_difficulty < 1.667:
                    quiz_difficulty = 1
                elif mean_difficulty > 2.333:
                    quiz_difficulty = 3
                else:
                    quiz_difficulty = 2
                new_quiz.difficulty = quiz_difficulty
                new_quiz.save()

    return render(
        request,
        "quiz/create.html",
        {"quiz_form": quiz_form, "tf_form": tf_formset, "mc_form": mc_formset},
    )


def load_sub_categories(request):
    category_id = request.GET.get("category")
    sub_categories = SubCategory.objects.filter(category_id=category_id).order_by(
        "sub_category"
    )
    return render(
        request,
        "quiz/subcategories_dropdown.html",
        {"sub_categories": sub_categories},
    )


class QuizListView(ListView):
    model = Quiz

class CategoryListView(ListView):
    model = Category

def quiz_list_by_category(request, category_name):
    category_id = Category.objects.get(category=category_name)
    quiz = Quiz.objects.filter(category=category_id)
    return render(request, "quiz/view_quiz_category.html", {'quiz': quiz})


class ViewQuizListByCategory(ListView):
    model = Quiz
    template_name = "view_quiz_category.html"

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(
            Category,
            category=self.kwargs['category_name']
        )

        return super(ViewQuizListByCategory, self).\
            dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ViewQuizListByCategory, self).\
            get_context_data(**kwargs)
        context["category"] = self.category
        print('\n\n',context["category"])
        return context

    def get_queryset(self):
        queryset = super(ViewQuizListByCategory, self).get_queryset()
        return queryset.filter(category=self.category)


def take(request):
    """
    get quiz
    get questions
    create 2 list of size n
    populate the first list with the questions
    populate the second list with the forms
    """
    if request.method == "GET":
        forms = []
        for i in range(3):
            forms.append(TotoForm(prefix="toto" + str(i)))

    if request.method == "POST":
        for i in range(3):
            toto = request
    return render(request, "quiz/take.html", {"forms": forms})


def take_quiz(request, url):
    quiz = Quiz.objects.get(url=url)
    tf_questions = TF_Question.objects.filter(quiz=quiz)
    mc_questions = MCQuestion.objects.filter(quiz=quiz)

    nb_tf_questions = tf_questions.count()
    nb_mc_questions = mc_questions.count()
    forms = [0] * (nb_tf_questions + nb_mc_questions)
    questions = [0] * (nb_tf_questions + nb_mc_questions)

    for question in tf_questions:
        index = question.order
        forms[index] = TFQuestionForm(prefix="tf" + str(index))
        questions[index] = question
    for question in mc_question:
        index = question.order
        forms[index] = MCQuestionForm(prefix="mc" + str(index))
        questions[index] = question

    if request.method == "GET":
        if quiz.ordered == False:
            questions = shuffle(questions)
        return render(request, "quiz/take_quiz.html")
    elif request.method == "POST":
        pass
