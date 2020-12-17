from collections import defaultdict, namedtuple

from true_false.models import TF_Question
from multichoice.models import MCQuestion
from quiz.models import AnswerUser


class Score:
    """
    Class used for keeping track of the user's good answers during the quiz.
    """
    def __init__(self):
        self.nb_good_answers = 0
        self.weighted = 0
        self.difficulty = {1: 0, 2: 0, 3: 0}
        self.theme = defaultdict(int)
        self.questions = []

    def add_correct_question(self, question):
        """
        Update the attribute's of the Score instance.
        """
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
    """
    Class used for keeping track of the properties of the quiz, wether
    the user answered well or not.
    """
    def __init__(self, nb_questions):
        self.weighted = 0
        self.difficulty = {1: 0, 2: 0, 3: 0}
        self.theme = defaultdict(int)
        self.nb_questions = nb_questions

    def populate(self, question):
        """
        Update the attribute's of the Total instance
        """
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
    """
    Class used to compute the customized advices to give to the user
    after he passed the quiz.
    """
    def __init__(self):
        self.advices = {}
        self.details = {}

    def _is_tf_answer_correct(self, tf_answer, question):
        """
        Returns True if the answer of the user is the same
        as the one chosen by the creator, returns False otherwise.
        """
        if tf_answer == str(question.correct):
            return True
        else:
            return False

    def _is_mc_answer_correct(self, mc_answer, question):
        """
        Returns True if the answer of the user is the same
        as the ones chosen by the creator, returns False otherwise.
        """
        if (
            mc_answer[0] == str(question.answer1_correct)
            and mc_answer[1] == str(question.answer2_correct)
            and mc_answer[2] == str(question.answer3_correct)
        ):
            return True
        else:
            return False

    def _update_or_create_answerUser(self, question, user, correct):
        """
        Create or Update the AnswerUser model with the user's answer.
        """
        try:
            answer_user = AnswerUser.objects.filter(question=question).get(user=user)
            answer_user.correct = correct
            answer_user.save()
        except AnswerUser.DoesNotExist:
            answer_user = AnswerUser(correct=correct)
            answer_user.save()
            answer_user.user.add(user)
            answer_user.question.add(question)
        return answer_user

    def _update_details_tf(self, well_answered, question, question_correct=True):
        """
        For each question, update self.details with a string telling
        the user if he/she answered well and if not, what was the correct answer
        """
        if well_answered:
            self.details[question.content] = "Vous avez bien répondu"
        else:
            if question_correct:
                self.details[question.content] = "La bonne réponse était Vrai"
            else:

                self.details[question.content] = "La bonne réponse était Faux"
        return self.details

    def _update_details_mc(self, well_answered, question=None):
        """
        For each question, update self.details with a string telling
        the user if he/she answered well and if not, what was the correct answer
        """
        if well_answered:
            self.details[question.content] = "Vous avez bien répondu"
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
        return self.details

    def statistics_tf(self, tf_answers, score, total, user):
        """
        Main function for the tf questions.
        It makes all the calls to the privates methods of the class
        for computing the results.
        """
        for qid, answer in tf_answers.items():
            question = TF_Question.objects.get(id=qid)
            total.populate(question)

            if self._is_tf_answer_correct(answer, question):
                score.add_correct_question(question)
                self._update_or_create_answerUser(question, user, True)
                self._update_details_tf(True, question)
            else:
                self._update_or_create_answerUser(question, user, False)
                self._update_details_tf(
                    False, question, question_correct=question.correct
                )

    def statistics_mc(self, mc_answers, score, total, user):
        """
        Main function for the mc questions.
        It makes all the calls to the privates methods of the class
        for computing the results.
        """
        for qid, answer in mc_answers.items():
            question = MCQuestion.objects.get(id=qid)
            total.populate(question)

            if self._is_mc_answer_correct(answer, question):
                score.add_correct_question(question)
                self._update_or_create_answerUser(question, user, True)
                self._update_details_mc(True, question=question)
            else:
                self._update_or_create_answerUser(question, user, False)
                self._update_details_mc(False, question=question)

    def _compute_nb_good_answers(self, nb_good_answers, nb_questions):
        """
        Updates self.advices to indicate the user the number
        of good answers he/she gave to the quiz.
        """
        self.advices["good_answers"] = (
            "Vous avez bien répondu à "
            + str(nb_good_answers)
            + " questions sur "
            + str(nb_questions)
        )

    def _compute_difficulty(self, score_difficulty, total_difficulty):
        """
        If the user's answers match certain patterns, give him customized
        advices.
        If he/she fails questions whatever their difficulties, propose him/her to
        begin to study the basics.
        If he/she answers well only to easy questions, propose him/her to tackle more
        difficult questions.
        If he/she answers well easy and medium questions, propose him/her to work on harder
        topics.
        Finally, if he/she answers well, just congratulate him/her.
        """
        if (
            score_difficulty[1] > total_difficulty[1] / 2
            and score_difficulty[2] > total_difficulty[2] / 2
            and score_difficulty[3] > total_difficulty[3] / 2
        ):
            self.advices[
                "difficulty"
            ] = "Vous maîtrisez très bien ce sujet, félicitations !"
        elif (
            score_difficulty[1] > total_difficulty[1] / 2
            and score_difficulty[2] > total_difficulty[2] / 2
            and score_difficulty[3] < total_difficulty[3] / 2
        ):
            self.advices[
                "difficulty"
            ] = "Vous maîtrisez bien ce sujet sujet mais les questions plus avancées vous échappent encore"
        elif (
            score_difficulty[1] > total_difficulty[1] / 2
            and score_difficulty[2] < total_difficulty[2] / 2
            and score_difficulty[3] < total_difficulty[3] / 2
        ):
            self.advices[
                "difficulty"
            ] = "Vous semblez maîtriser les bases, poursuivez vos efforts !"
        elif (
            score_difficulty[1] < total_difficulty[1] / 2
            and score_difficulty[2] < total_difficulty[2] / 2
            and score_difficulty[3] < total_difficulty[3] / 2
        ):
            self.advices[
                "difficulty"
            ] = "Vous ne semblez pas maîtriser le sujet. Commencez par revoir les bases."

    def _compute_theme(self, themes, total_themes):
        """
        For each theme in the quiz, compute if the user answered well or not,
        advises the user if he/she should work on them or not.
        """
        for theme, score in themes.items():
            if score > total_themes[theme] / 2:
                self.advices[
                    theme
                ] = "Vous avez bien réussi les questions sur le thème : " + str(theme)
            else:
                self.advices[
                    theme
                ] = "Vous devriez réviser le sujet suivant : " + str(theme)

    def compute_scores(self, score, total):
        """
        Call the methods to compute the number of good answers given, 
        the success according to the question's difficulty, and
        according to questions themes.
        """

        # nb good answers
        self._compute_nb_good_answers(score.nb_good_answers, total.nb_questions)

        # difficulty
        self._compute_difficulty(score.difficulty, total.difficulty)

        # theme
        self._compute_theme(score.theme, total.theme)
