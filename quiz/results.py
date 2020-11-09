from collections import defaultdict

from true_false.models import TF_Question
from multichoice.models import MCQuestion

def results(tf_answers, mc_answers, total_questions):
    nb_good_answers = 0
    weighted_score = 0
    score_difficulty = {1: 0, 2: 0, 3: 0}
    total_difficulty = defaultdict(int)
    total_theme = defaultdict(int)
    score_theme = defaultdict(int)
    total_score = 0

    results_dict = {}

    # tf answers
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
        
        # check correct questions
        if answer == str(question.correct):
            nb_good_answers += 1
            weighted_score += question.difficulty
            score_difficulty[question.difficulty] += 1
            if theme1:
                score_theme[theme1] += 1
            if theme2:
                score_theme[theme2] += 1
            if theme3:
                score_theme[theme3] += 1
        
    for qid, answers in mc_answers.items():
        question = MCQuestion.objects.get(id=qid)

        total_score += question.difficulty
        total_difficulty[question.difficulty] += 1
        theme1, theme2, theme3 = question.theme1, question.theme2, question.theme3

        if theme1:
            total_theme[theme1] += 1
        if theme2:
            total_theme[theme2] += 1
        if theme3:
            total_theme[theme3] += 1

        # check correct questions
        if (
            answers[0] == str(question.answer1_correct)
            and answers[1] == str(question.answer2_correct)
            and answers[2] == str(question.answer3_correct)
        ):
            nb_good_answers += 1
            weighted_score += question.difficulty
            score_difficulty[question.difficulty] += 1
            if theme1:
                score_theme[theme1] += 1
            if theme2:
                score_theme[theme2] += 1
            if theme3:
                score_theme[theme3] += 1

    if weighted_score/total_score > 0.66:
        "Vous avez très bien réussi le quiz !"
    elif weighted_score/total_score < 0.33:
        results_dict["global"] = "Vous avez besoin de plus de révisions, courage !"
    else:
        results_dict["global"] = "Avec un peu de travail supplémentaire, vous réussirez !"

    results_dict["detail_answers"] = \
        ("Vous avez bien répondu à " +
        str(nb_good_answers) + 
        " questions sur " + 
        str(total_questions)
    )

    for diff, score in score_difficulty.items():
        results_dict[diff] = \
            ("Vous avez bien répondu à " +
            str(score) +
            str(" questions de difficulté ") + str(diff) + " sur "+
            str(total_difficulty[diff])
        )

    if (score_difficulty[1] > total_difficulty[1]/2 and
        score_difficulty[2] > total_difficulty[2]/2 and
        score_difficulty[3] > total_difficulty[3]/2):
        results_dict["difficulty"] = "Vous avez bien réussi toutes les difficultés"
    elif (score_difficulty[1] > total_difficulty[1]/2 and
        score_difficulty[2] > total_difficulty[2]/2 and
        score_difficulty[3] < total_difficulty[3]/2):
        results_dict["difficulty"] = "Tout réussi sauf le difficile"
    elif (score_difficulty[1] > total_difficulty[1]/2 and
        score_difficulty[2] < total_difficulty[2]/2 and
        score_difficulty[3] < total_difficulty[3]/2):
        results_dict["difficulty"] = "Seul le facile est réussi"

    for theme, score in score_theme.items():
        if score > total_theme[theme]/2:
            results_dict[str(theme)] = "Thème " + str(theme) + " réussi"
        else:
            results_dict[str(theme)] = "Thème " + str(theme) + " raté"


    for diff, score in score_difficulty.items():
        if score > total_difficulty[diff]/2:
            results_dict["difficulty"+str(diff)] = "Vous avez réussi en difficulté " + str(diff)
        else:
            results_dict["difficulty"+str(diff)] = "Vous avez raté en difficulté " + str(diff)
    for key, val in results_dict.items():
        print(key, "\n", val)
        print("---------------------------------")