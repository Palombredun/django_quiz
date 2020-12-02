from collections import defaultdict, namedtuple

from true_false.models import TF_Question
from multichoice.models import MCQuestion
from quiz.models import AnswerUser


class Score:
    def __init__(self):
        self.nb_good_answers = 0
        self.weighted = 0
        self.difficulty = {1: 0, 2: 0, 3: 0}
        self.theme = defaultdict(int)
        self.questions = []

    def add_correct_question(self, question):
        self.nb_good_answers += 1
        self.weighted += question.difficulty
        self.difficulty[question.difficulty] += 1
        self.questions.append(question)

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
        self.difficulty = {1: 0, 2: 0, 3: 0}
        self.theme = defaultdict(int)
        self.nb_questions = nb_questions

    def populate(self, question):
        self.weighted += question.difficulty
        self.difficulty[question.difficulty] += 1

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

    def _is_tf_answer_correct(self, tf_answer, question):
        if tf_answer == str(question.correct):
            return True
        else:
            return False

    def _is_mc_answer_correct(self, mc_answer, question):
        if (
            mc_answer[0] == str(question.answer1_correct)
            and mc_answer[1] == str(question.answer2_correct)
            and mc_answer[2] == str(question.answer3_correct)
        ):
            return True
        else:
            return False

    def _update_or_create_answerUser(self, question, user, correct):
        try:
            answer_user = AnswerUser.objects.filter(question=question).get(user=user)
            answer_user.correct = correct
            answer_user.save()
        except AnswerUser.DoesNotExist:
            answer_user = AnswerUser(correct=correct)
            answer_user.save()
            answer_user.user.add(user)
            answer_user.question.add(question)
        

    def _update_details_tf(self, well_answered, question, question_correct=None):
        if well_answered:
            self.details[question.content] = "Vous avez bien répondu"
        else:
            if question_correct:
                self.details[question.content] = "La bonne réponse était Vrai"
            else:
                self.details[question.content] = "La bonne réponse était Vrai"

    def _update_details_mc(self, well_answered, question=None):
        if well_answered:
            self.self.details[question.content] = "Vous avez bien répondu"
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

    def statistics_tf(self, tf_answers, score, total, user):
        for qid, answer in tf_answers.items():
            question = TF_Question.objects.get(id=qid)
            total.populate(question)

            if self._is_tf_answer_correct(answer, question):
                score.add_correct_question(question)
                self._update_or_create_answerUser(question, user, True)
                self._update_details_tf(True, question)
            else:
                self._update_or_create_answerUser(question, user, False)
                self._update_details_tf(False, question, question_correct=question.correct)

    def statistics_mc(self, mc_answers, score, total, user):
        for qid, answer in mc_answers.items():
            question = MCQuestion.objects.get(id=qid)
            total.populate(question)

            if self._is_mc_question_correct(answer, question):
                score.add_correct_question(question)
                self.update_or_create_answerUser(question, user, True)
                self.update_details_mc(True, question=question)
            else:
                self.update_or_create_answerUser(question, user, False)
                self.update_details_mc(False, question=question)

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
