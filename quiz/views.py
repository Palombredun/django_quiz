from random import shuffle
import logging

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.forms import formset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.views.generic.list import ListView

from quiz.forms import QuizForm
from multichoice.forms import CreationMultiChoiceForm, MultiChoiceForm
from true_false.forms import CreationTrueFalseForm, TrueFalseForm


from quiz.models import (
    Quiz,
    Question,
    Category,
    SubCategory,
    Statistic,
    Grade,
    QuestionScore,
    ThemeScore,
)
from true_false.models import TF_Question
from multichoice.models import MCQuestion

from quiz.results import Result, Score, Total


logger = logging.getLogger(__name__)

def tutorial(request):
    """
    Tutorial page explaining to the user what each field means.
    """
    logger.info("{levelname} {asctime} - User accessed tutorial page")
    response = render(request, "quiz/tutorial.html")
    response.set_cookie("tutorial", "True")
    return response


@login_required
def create(request):
    """
    View dedicated to the creation of the quiz using formsets.
    The user has to add at least one question for it to be valid.
    """
    TF_Formset = formset_factory(CreationTrueFalseForm)
    MC_Formset = formset_factory(CreationMultiChoiceForm)
    
    if request.method == "GET":
        logger.info("{levelname} {asctime} - User accessed create page")

        quiz_form = QuizForm(request.GET or None, prefix="quiz")
        tf_formset = TF_Formset(request.GET or None, prefix="tf")
        mc_formset = MC_Formset(request.GET or None, prefix="mc")
    
    elif request.method == "POST":
        logger.info("{levelname} {asctime} - User wants to create a quiz")

        quiz_form = QuizForm(request.POST, prefix="quiz")
        tf_formset = TF_Formset(request.POST or None, prefix="tf")
        mc_formset = MC_Formset(request.POST or None, prefix="mc")

        if quiz_form.is_valid() and ((tf_formset.is_valid() and mc_formset.is_valid())):
            logger.info("{levelname} {asctime} - Quiz is valid")
            quiz_cd = quiz_form.cleaned_data

            category = Category.objects.get(id=quiz_cd["category"])
            category_name = (
                category.category.replace(" ", "-").replace("ç", "c").replace("é", "e")
            )
            if quiz_cd["sub_category"]:
                sub_category = SubCategory.objects.get(id=quiz_cd["sub_category"])
            else:
                sub_category = None
            new_quiz = Quiz(
                title=quiz_cd["title"],
                description=quiz_cd["description"],
                creator=request.user,
                url="placeholder",
                category=category,
                category_name=category_name,
                sub_category=sub_category,
                random_order=quiz_cd["random_order"],
                difficulty=0,
            )
            new_quiz.save()

            mean_difficulty = 0
            n = 0

            if tf_formset:
                for question in tf_formset:
                    cd = question.cleaned_data
                    n += 1
                    mean_difficulty += int(cd["difficulty"])

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

            if mc_formset:
                for question in mc_formset:
                    cd = question.cleaned_data
                    n += 1
                    mean_difficulty += int(cd["difficulty"])
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
            
            mean_difficulty /= n
            # Calculation of the difficulty
            if mean_difficulty < 1.667:
                quiz_difficulty = 1
            elif mean_difficulty > 2.333:
                quiz_difficulty = 3
            else:
                quiz_difficulty = 2
            new_quiz.difficulty = quiz_difficulty

            new_quiz.url = slugify(quiz_cd["title"]) + "-" + str(new_quiz.id)
            new_quiz.save()

            return redirect("profile")

    return render(
        request,
        "quiz/create.html",
        {"quiz_form": quiz_form, "tf_form": tf_formset, "mc_form": mc_formset},
    )


def load_sub_categories(request):
    """
    View called by the dependent dropdown list of categories.
    """
    category_id = request.GET.get("category")
    sub_categories = SubCategory.objects.filter(category_id=category_id).order_by(
        "sub_category"
    )
    logger.info("{levelname} {asctime} - Subcategories requested in page create")
    return render(
        request, "quiz/subcategories_dropdown.html", {"sub_categories": sub_categories}
    )


def quiz_list(request):
    """
    View returning all the quiz ordered by their date of creation.
    """
    logger.info("{levelname} {asctime} - User accessed quiz-list page")
    quiz_list = Quiz.objects.all().order_by("-created")
    categories = Category.objects.all()
    return render(
        request,
        "quiz/quiz_list.html",
        {"quiz_list": quiz_list, "categories": categories},
    )


def quiz_list_by_category(request, category_name):
    """
    View return all the quiz from the category specified in the url
    ordered by their date of creation
    """
    logger.info("{levelname} {asctime} - User accessed quiz-by-category page")
    category = get_object_or_404(Category, category=category_name)
    subcategories = SubCategory.objects.filter(category=category)
    quiz = Quiz.objects.filter(category=category)
    return render(
        request,
        "quiz/view_quiz_category.html",
        {"category": category_name, 
        "subcategories": subcategories, 
        "quiz_list": quiz},
    )


def quiz_list_by_subcategory(request, subcategory_name):
    """
    View return all the quiz from the subcategory specified in the url
    ordered by their date of creation
    """
    logger.info("{levelname} {asctime} - User accessed quiz-by-subcategory page")
    subcategory_id = get_object_or_404(SubCategory, sub_category=subcategory_name)
    quiz = Quiz.objects.filter(sub_category=subcategory_id)
    return render(
        request,
        "quiz/view_quiz_subcategory.html",
        {"sub_category": subcategory_name,
        "subcategories": subcategory_name, 
        "quiz_list": quiz},
    )


@login_required
def take(request, url):
    """
    Send questions belonging to the quiz
    Receive results, compare them to the answers,
    redirect to page results
    """
    quiz = get_object_or_404(Quiz, url=url)
    tf_questions = TF_Question.objects.filter(quiz=quiz).order_by("order")
    mc_questions = MCQuestion.objects.filter(quiz=quiz).order_by("order")


    total_questions = tf_questions.count() + mc_questions.count()
    forms = [0] * total_questions

    tf_prefix = []
    for question in tf_questions:
        index = question.order
        prefix = "tf" + str(index)
        forms[index] = (
            "tf",
            question.content,
            TrueFalseForm(
                request.GET or None,
                initial={"qid": question.id},
                prefix=prefix,
            ),
        )
        tf_prefix.append(prefix)
    
    mc_prefix = []
    for question in mc_questions:
        index = question.order
        prefix = "mc" + str(index)
        forms[index] = (
            "mc",                           
            question.content,               
            question.answer1,               
            question.answer2,               
            question.answer3,               
            MultiChoiceForm(  
                request.GET or None,              
                initial={"qid": question.id},
                prefix=prefix,
            ),
        )
        mc_prefix.append(prefix)

    if request.method == "GET":
        logger.info("{levelname} {asctime} - User accessed take page for the quiz " + str(url))
        
        if quiz.random_order is True:
            shuffle(forms)
        return render(
            request,
            "quiz/take.html",
            {"title": quiz.title, "description": quiz.description, "forms": forms},
        )


    elif request.method == "POST":
        logger.info("{levelname} {asctime} - User finished the quiz " + str(url))
        tf_answers = {}
        while tf_prefix:
            prefix = tf_prefix.pop()
            tf = TrueFalseForm(request.POST or None, prefix=prefix)
            if tf.is_valid():
                cd = tf.cleaned_data
                tf_answers[cd["qid"]] = cd["correct"]
        
        mc_answers = {}
        while mc_prefix:
            prefix = mc_prefix.pop()
            mc = MultiChoiceForm(request.POST or None, prefix=prefix)
            if mc.is_valid():
                cd = mc.cleaned_data
                mc_answers[cd["qid"]] = (cd["answer1"], cd["answer2"], cd["answer3"])
        
        # compute the student's score of the quiz
        results_user = Score()
        total_score = Total(total_questions)
        results = Result()

        results.statistics_tf(tf_answers, results_user, total_score, request.user)
        results.statistics_mc(mc_answers, results_user, total_score, request.user)
        results.compute_scores(results_user, total_score)

        grade_user = round(results_user.nb_good_answers * 10 / total_score.nb_questions)
        questions = results_user.questions

        stats, created = Statistic.objects.get_or_create(quiz=quiz)
        stats.number_participants += 1
        stats.mean += results_user.nb_good_answers / stats.number_participants
        stats.easy += results_user.difficulty[1]
        stats.medium += results_user.difficulty[2]
        stats.difficult += results_user.difficulty[3]
        stats.save()

        # save the user's results
        try:
            g = Grade.objects.filter(statistics=stats).get(grade=grade_user)
            g.number += 1
        except Grade.DoesNotExist:
            g = Grade(grade=grade_user, number=1, statistics=stats)
        g.save()

        for question in questions:
            try:
                q = QuestionScore.objects.get(question=question)
                q.score += 1
            except QuestionScore.DoesNotExist:
                q = QuestionScore(question=question, score=1, statistics=stats)
            q.save()

        for theme, score in results_user.theme.items():
            try:
                t = ThemeScore.objects.filter(quiz=quiz).get(theme=theme)
                t.score += 1
            except ThemeScore.DoesNotExist:
                t = ThemeScore(theme=theme, score=1, quiz=quiz, statistics=stats)
            t.save()

        return render(
            request,
            "quiz/results.html",
            {"details": results.details, "advices": results.advices},
        )


@login_required
def statistics(request, url):
    """
    If the user is the creator of the quiz,
    send him the results to the quiz he asked.
    """
    quiz = get_object_or_404(Quiz, url=url)
    if request.user == quiz.creator:
        logger.info("{levelname} {asctime} - Creator of the quiz " + str(url) + "accessed the page")
        try:
            stats = Statistic.objects.get(quiz=quiz)

            grades = Grade.objects.filter(statistics=stats).order_by("grade")
            grades_label = []
            grades_data = []
            for grade in grades:
                grades_label.append(grade.grade)
                data = round(100 * (grade.number / stats.number_participants))
                grades_data.append(data)

            questions = QuestionScore.objects.filter(statistics=stats).order_by(
                "question__order"
            )
            questions_label = []
            questions_data = []
            for question in questions:
                questions_label.append(question.question.content)
                data = round(100 * (question.score / stats.number_participants))
                questions_data.append(data)

            qs = Question.objects.filter(quiz=quiz)
            themes = ThemeScore.objects.filter(statistics=stats).filter(quiz=quiz)
            themes_label = []
            themes_data = []
            for theme in themes:
                themes_label.append(theme.theme)
                theme_occurences = sum(
                    [
                        len(qs.filter(theme1=theme.theme)),
                        len(qs.filter(theme2=theme.theme)),
                        len(qs.filter(theme3=theme.theme)),
                    ]
                )
                data = round(100 * (theme.score / theme_occurences))
                themes_data.append(theme.score)

            total_difficulty = {1: 0, 2: 0, 3: 0}
            for question in qs:
                total_difficulty[question.difficulty] += 1
            score_difficulty = {1: stats.easy, 2: stats.medium, 3: stats.difficult}
            stats = {
                "mean": stats.mean,
                "nb_participants": stats.number_participants,
                "difficulty": [
                    round(100 * diff/total)
                    for diff, total in zip(score_difficulty.values(), total_difficulty.values())
                    if total != 0
                ] 
            }

            return render(
                request,
                "quiz/statistics.html",
                {
                    "title": quiz.title,
                    "stats": stats,
                    "g_label": grades_label,
                    "g_data": grades_data,
                    "q_label": questions_label,
                    "q_data": questions_data,
                    "t_label": themes_label,
                    "t_data": themes_data,
                },
            )
        except Statistic.DoesNotExist:
            return render(
                request,
                "quiz/statistics.html",
                {"message": "Personne n'a passé ce quiz pour le moment"},
            )
    else:
        return redirect("profile")
