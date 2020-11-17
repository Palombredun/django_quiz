from collections import defaultdict, namedtuple

from true_false.models import TF_Question
from multichoice.models import MCQuestion


class Score:
    def __init__(self):
        self.nb_good_answers = 0
        self.weighted = 0
        self.difficulty = {1: 0, 2: 0, 3: 0}
        self.theme = defaultdict(int)

    def add_correct_question(self, question):
        self.nb_good_answers += 1
        self.weighted += question.difficulty
        self.difficulty[question.difficulty] += 1

        theme1, theme2, theme3 = question.theme1, question.theme2, question.theme3
        if theme1:
            self.theme[theme1] += 1
        if theme2:
            self.theme[theme2] += 1
        if theme3:
            self.theme[theme3] += 1


class Total:
    def __init__(self, nb_questions):
        self.weighted = 0
        self.difficulty = defaultdict(int)
        self.theme = defaultdict(int)
        self.nb_questions = nb_questions

    def populate(self, question):
        self.weighted += question.difficulty
        self.difficulty[question.difficulty]

        theme1, theme2, theme3 = question.theme1, question.theme2, question.theme3
        if theme1:
            self.theme[theme1] += 1
        if theme2:
            self.theme[theme2] += 1
        if theme3:
            self.theme[theme3] += 1


class Result:
    def __init__(self):
        self.advices = {}
        self.details = {}

    def statistics_tf(self, tf_answers, score, total):
        for qid, answer in tf_answers.items():
            question = TF_Question.objects.get(id=qid)
            total.populate(question)

            if answer == str(question.correct):
                self.details[question.content] = "Vous avez bien répondu"
                score.add_correct_question(question)
            else:
                if question.correct == True:
                    self.details[question.content] = "La bonne réponse était Vrai"
                elif question.correct == False:
                    self.details[question.content] = "La bonne réponse était Faux"

    def statistics_mc(self, mc_answers, score, total):
        for qid, answer in mc_answers.items():
            question = MCQuestion.objects.get(id=qid)
            total.populate(question)

            if (
                answers[0] == str(question.answer1_correct)
                and answers[1] == str(question.answer2_correct)
                and answers[2] == str(question.answer3_correct)
            ):
                self.details[question.content] = "Vous avez bien répondu"
                score.add_correct_question(question)
            else:
                answers = []
                if question.answer1_correct == True:
                    answers.append(question.answer1)
                if question.answer2_correct == True:
                    answers.append(question.answer2)
                if question.answer3_correct == True:
                    answers.append(question.answer3)
                tmp = "\n"
                for answer in answers:
                    tmp += answer + "\n"
                self.details[question.content] = "La bonne réponse était : " + tmp

    def compute_scores(self, score, total):
        if score.weighted / total.weighted > 0.66:
            self.advices["global"] = "Vous avez très bien réussi le quiz !"
        elif score.weighted / total.weighted < 0.33:
            self.advices["global"] = "Vous avez besoin de plus de révisions, courage !"
        else:
            self.advices[
                "global"
            ] = "Avec un peu de travail supplémentaire, vous réussirez !"

        self.advices["good_answers"] = (
            "Vous avez bien répondu à "
            + str(score.nb_good_answers)
            + " questions sur "
            + str(total.nb_questions)
        )

        if (
            score.difficulty[1] > total.difficulty[1] / 2
            and score.difficulty[2] > total.difficulty[2] / 2
            and score.difficulty[3] > total.difficulty[3] / 2
        ):
            self.advices[
                "difficulty"
            ] = "Vous maîtrisez très bien ce sujet, félicitations !"
        elif (
            score.difficulty[1] > total.difficulty[1] / 2
            and score.difficulty[2] > total.difficulty[2] / 2
            and score.difficulty[3] < total.difficulty[3] / 2
        ):
            self.advices[
                "difficulty"
            ] = "Vous maîtrisez bien ce sujet sujet mais les questions plus avancées vous échappent encore"
        elif (
            score.difficulty[1] > total.difficulty[1] / 2
            and score.difficulty[2] < total.difficulty[2] / 2
            and score.difficulty[3] < total.difficulty[3] / 2
        ):
            self.advices[
                "difficulty"
            ] = "Vous semblez maîtriser les bases, poursuivez vos efforts !"

        for theme, score in score.theme.items():
            if score > total.theme[theme] / 2:
                self.advices[
                    str(theme)
                ] = "Vous avez bien réussi les questions sur le thème " + str(theme)
            else:
                self.advices[
                    str(theme)
                ] = "Vous devriez réviser le sujet suivant " + str(theme)