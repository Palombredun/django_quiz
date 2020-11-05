from collections import defaultdict

from true_false.models import TF_Question
from multichoice.models import MCQuestion

def results(tf_answers, mc_answers, total_questions):
    nb_good_answers = 0
    myscore = 0
    score_difficulty = defaultdict(int)
    total_difficulty = defaultdict(int)
    total_theme = defaultdict(int)
    score_theme = defaultdict(int)
    total_score = 0
    for qid, answer in tf_answers.items():
        question = TF_Question.objects.get(id=qid)

        total_score += question.difficulty
        total_difficulty[question.difficulty] += 1
        theme1, theme2, theme3 = question.theme1, question.theme2, question.theme3
        if theme1:
            total_theme[theme1] += 1
        if theme2:
            total_theme[theme2] += 1
        if theme3:
            total_theme[theme3] += 1
            
        if answer == str(question.correct):
            nb_good_answers += 1
            myscore += question.difficulty
            score_difficulty[question.difficulty] += 1
            if theme1:
                score_theme[theme1] += 1
            if theme2:
                score_theme[theme2] += 1
            if theme3:
                score_theme[theme3] += 1
        
    for qid, answers in mc_answers.items():
        question = MCQuestion.objects.get(id=qid)
        total_difficulty[question.difficulty] += 1
        if (
            answers[0] == str(question.answer1_correct)
            and answers[1] == str(question.answer2_correct)
            and answers[2] == str(question.answer3_correct)
        ):
            nb_good_answers += 1
            score_difficulty[question.difficulty] += 1
    print("---------------------------")
    if myscore/total_score > 0.66:
        print("Vous avez très bien réussi le quiz !")
    elif myscore/total_score < 0.33:
        print("Vous avez besoin de plus de révisions, courage !")
    else:
        print("Avec un peu de travail supplémentaire, vous réussirez !")
    print("---------------------------")
    print(
        "Vous avez bien répondu à",
        nb_good_answers,
        "questions sur",
        total_questions,
    )
    print("---------------------------")
    for diff, score in score_difficulty.items():
        print(
            "Vous avez bien répondu à",
            score,
            "questions de difficulté", diff, "sur",
            total_difficulty[diff],
        )
    print("---------------------------")
    for theme, score in score_theme.items():
        print(
            "Vous avez bien répondu à",
            score,
            "questions", theme, "sur",
            total_theme[theme]
        )
        print("###")
    print("---------------------------")
    if nb_good_answers > total_questions/2:
        print("Vous avez globalement bien réussi le quiz")
    else:
        print("Vous avez globalement raté le quiz")
    for diff, score in score_difficulty.items():
        if score > total_difficulty[diff]/2:
            print("Vous avez réussi en difficulté", diff)
        else:
            print("Vous avez raté en difficulté")
    for theme, score in score_theme.items():
        if score > total_theme[theme]/2:
            print("Vous avez réussi le thème", theme)
        else:
            print("Vous avez raté le thème", theme)