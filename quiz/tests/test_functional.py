from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User

import pytest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from time import sleep
from datetime import datetime

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

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestCreateQuiz(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

        # Create Categories and SubCategories
        sc = Category.objects.create(category="Sciences")
        ph = SubCategory.objects.create(category=sc, sub_category="Physique")
        ch = SubCategory.objects.create(category=sc, sub_category="Chimie")
        svt = SubCategory.objects.create(category=sc, sub_category="Sciences de la Vie et de la Terre")
        bio = SubCategory.objects.create(category=sc, sub_category="Biologie")
        info = SubCategory.objects.create(category=sc, sub_category="Informatique")
        tec = SubCategory.objects.create(category=sc, sub_category="Technologie")
        si = SubCategory.objects.create(category=sc, sub_category="Sciences de l'Ingénieur")
        math = SubCategory.objects.create(category=sc, sub_category="Mathématiques")
        sc_au = SubCategory.objects.create(category=sc, sub_category="Autres")
        
        fr = Category.objects.create(category="Francais")
        ortho = SubCategory.objects.create(category=fr, sub_category="Orthographe")
        gram = SubCategory.objects.create(category=fr, sub_category="Grammaire")
        voc = SubCategory.objects.create(category=fr, sub_category="Vocabulaire")
        lit = SubCategory.objects.create(category=fr, sub_category="Littérature")
        fr_au = SubCategory.objects.create(category=fr, sub_category="Autres")
        
        lg = Category.objects.create(category="Langues")
        an = SubCategory.objects.create(category=lg, sub_category="Anglais")
        it = SubCategory.objects.create(category=lg, sub_category="Italien")
        es = SubCategory.objects.create(category=lg, sub_category="Espagnol")
        de = SubCategory.objects.create(category=lg, sub_category="Allemand")
        po = SubCategory.objects.create(category=lg, sub_category="Portugais")
        lg_au = SubCategory.objects.create(category=lg, sub_category="Autres")
        
        hg = Category.objects.create(category="Histoire-Geographie")
        hi = SubCategory.objects.create(category=hg, sub_category="Histoire"),
        geo = SubCategory.objects.create(category=hg, sub_category="Géographie"),
        emc = SubCategory.objects.create(category=hg, sub_category="Enseignement Moral et Civique"),
        ses = SubCategory.objects.create(category=hg, sub_category="Sciences Economiques et Sociales")
        hg_au = lg_au = SubCategory.objects.create(category=hg, sub_category="Autres")
        
        au = Category.objects.create(category="Autres")

        # create a user :
        user_A = User.objects.create_user(
            username="A",
            email="a@mail.com",
            password="_MyKindOfPassword123_"
        )

        # create a quiz :
        quiz = Quiz(
            title="Titre du quiz",
            description="Quiz crée pour les tests fonctionnels",
            creator=user_A,
            url="titre-du-quiz-1",
            category=sc,
            category_name="Sciences",
            sub_category=ph,
            random_order=False,
            created=datetime.now(),
            difficulty=2
        )
        quiz.save()

        tf1=TF_Question.objects.create(
            quiz=quiz,
            difficulty=1,
            order=0,
            content="Question 1",
            theme1="t1",
            theme2="t2",
            theme3="",
            correct=True)
        mc1 = MCQuestion.objects.create(
            quiz=quiz,
            difficulty=2,
            order=1,
            content="Question 2",
            theme1="t1",
            theme2="t3",
            theme3="",
            answer1="réponse fausse",
            answer1_correct=False,
            answer2="réponse vraie",
            answer2_correct=True,
            answer3="réponse vraie",
            answer3_correct=True)
        tf2=TF_Question.objects.create(
            quiz=quiz,
            difficulty=3,
            order=2,
            content="Question 3",
            theme1="t1",
            theme2="t2",
            theme3="t3",
            correct=False
        )

    def tearDown(self):
        self.browser.quit()

    def login(self):
        login_link = self.browser.find_element_by_id("login")
        login_link.click()
        username_input = self.browser.find_element_by_id("id_username")
        username_input.send_keys("A")
        password_input = self.browser.find_element_by_id("id_password")
        password_input.send_keys("_MyKindOfPassword123_")
        button = self.browser.find_element_by_id("login_button")
        button.click()


    def test_take_quiz(self):
        """
        Assert that a quiz created by the user is present in his profile
        both in the qui created and in the quiz finished once he passed it.
        """
        # Visit the website
        self.browser.get(self.live_server_url)

        # Login
        self.login()
        
        # Visit the profile
        profile_link = self.browser.find_element_by_id("profile")
        profile_link.click()

        # Assert the quiz is in created list
        show_created = self.browser.find_element_by_id("created")
        show_created.click()
        quiz_url = self.browser.find_element_by_id("titre-du-quiz-1")
        assert quiz_url.text == "Titre du quiz"
        quiz_url.click()

        # check that no one passed the quiz
        assert self.browser.title == "Statistiques"
        message = self.browser.find_element_by_id("message")
        assert message.text == "Personne n'a passé ce quiz pour le moment"

        # Visit the quiz-list page to pass our own quiz
        quiz_list = self.browser.find_element_by_id("quiz_list")
        quiz_list.click()
        assert self.browser.title == "Liste des quiz"

        # assert our quiz is in the list
        my_quiz = self.browser.find_element_by_id("titre-du-quiz-1")
        assert my_quiz.text == "Titre du quiz"

        # Visit the category page Langues to see if a quiz exists in this category
        show_categories = self.browser.find_element_by_id("show-categories")
        show_categories.click()
        langues_link = self.browser.find_element_by_id("Langues")
        langues_link.click()
        assert self.browser.title == "Langues"

        # Back to the quiz list, visit the Sciences category list page
        self.browser.back()
        show_categories = self.browser.find_element_by_id("show-categories")
        show_categories.click()
        sciences_link = self.browser.find_element_by_id("Sciences")
        sciences_link.click()
        assert self.browser.title == "Sciences"
        # assert the quiz is in the Sciences category
        quiz_url = self.browser.find_element_by_id("titre-du-quiz-1")
        assert quiz_url.text == "Titre du quiz"

        # Visit the Physique subcategory list page
        show_categories = self.browser.find_element_by_id("show-categories")
        show_categories.click()
        math_link = self.browser.find_element_by_id("Physique")
        math_link.click()
        assert self.browser.title == "Physique"
        # assert the quiz is in the Physique subcategory
        quiz_url = self.browser.find_element_by_id("titre-du-quiz-1")
        assert quiz_url.text == "Titre du quiz"

        self.browser.get(self.live_server_url + "/quiz/take/titre-du-quiz-1")
        assert self.browser.title == "Titre du quiz"

        answer_tf1 = Select(self.browser.find_element_by_id("id_tf0-correct"))
        #answer_tf1.select_by_visible_text("Vrai")
        answer_tf1.select_by_visible_text("Faux")

        user_answer_mc1 = self.browser.find_element_by_id("id_mc1-answer2")
        user_answer_mc1.click()
        user_answer_mc1 = self.browser.find_element_by_id("id_mc1-answer3")
        user_answer_mc1.click()

        answer_tf2 = Select(self.browser.find_element_by_id("id_tf2-correct"))
        answer_tf2.select_by_visible_text("Vrai")

        submit = self.browser.find_element_by_id("submit")
        submit.click()

        # assert we're still on the same page
        sleep(5)
        assert self.browser.title == "Résultat"

        sleep(500)



        

    @pytest.mark.skip(reason="no way of currently testing this")
    def test_create_quiz(self):
        """
        GIVEN a user who wants to create a quiz
        WHEN he lands on the quiz creation page
        THEN assert the he can create the quiz he wants
        """

        self.browser.get(self.live_server_url)

        # the user begins by logging in
        self.login()

        # the user uses the link in the home page to create a quiz
        create_button = self.browser.find_element_by_id("create-quiz")
        create_button.click()

        # the user has to login first
        username_input = self.browser.find_element_by_id("id_username")
        username_input.send_keys("A")
        password_input = self.browser.find_element_by_id("id_password")
        password_input.send_keys("_MyKindOfPassword123_")
        button = self.browser.find_element_by_id("login_button")
        button.click()

        assert self.browser.title == "Créer un quiz"

        # Since it's the first time the user is creating a quiz, he visits the tutorial
        tutorial = self.browser.find_element_by_id("tutorial")
        tutorial.click()

        assert self.browser.title == "Tutorial"

        # get back to create a quiz
        back_to_create = self.browser.find_element_by_id("create-quiz")
        back_to_create.click()

        # Basic elements of the quiz :
        quiz_title = self.browser.find_element_by_id("id_quiz-title")
        quiz_title.send_keys("Le théorème de Pythagore")
        quiz_description = self.browser.find_element_by_id("id_quiz-description")
        quiz_description.send_keys("Ce qui a pour but but de vérifier les connaissances \
            des participants sur le théorème de Pythagore.")
        quiz_category = Select(self.browser.find_element_by_id("id_quiz-category"))
        quiz_category.select_by_visible_text('Sciences')
        self.browser.implicitly_wait(1)
        quiz_subcategory = Select(self.browser.find_element_by_id("id_quiz-sub_category"))
        quiz_subcategory.select_by_visible_text("Mathématiques")

        # add a first MC question :
        add_mc = self.browser.find_element_by_id("add-mc")
        add_mc.click()
        self.browser.implicitly_wait(1)
        mc1_content = self.browser.find_element_by_id("forms")
        #mc1_content.send_keys("Le théorème de Pythagore concerne")

