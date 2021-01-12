from django.contrib.staticfiles.testing import StaticLiveServerTestCase

import pytest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options


class TestProfile(StaticLiveServerTestCase):
    def setUp(self):
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(options=options)

    def tearDown(self):
        self.browser.quit()

    def test_profile_page(self):
        """
        GIVEN a user who has an account and wants to visit his/her profile
        WHEN they login and visit their profile
        THEN assert the page and the good informations are sent. 

        The case where a user has created and passed a quiz is tested in quiz app
        """
        self.browser.get(self.live_server_url)
        
        # visit the register page
        login = self.browser.find_element_by_id("login")
        login.click()
        register = self.browser.find_element_by_id("register")
        register.click()

        # create an account
        username_input = self.browser.find_element_by_id("id_username")
        username_input.send_keys("A")
        email_input = self.browser.find_element_by_id("id_email")
        email_input.send_keys("a@mail.com")
        password_input = self.browser.find_element_by_id("id_password")
        password_input.send_keys("_MyKindOfPassword123_")
        password2_input = self.browser.find_element_by_id("id_password2")
        password2_input.send_keys("_MyKindOfPassword123_")
        button = self.browser.find_element_by_id("register")
        button.click()

        # assert we have been properly redirected to the login page
        assert self.browser.title == "Connexion"

        # login with our credentials
        username_input = self.browser.find_element_by_id("id_username")
        username_input.send_keys("A")
        password_input = self.browser.find_element_by_id("id_password")
        password_input.send_keys("_MyKindOfPassword123_")
        button = self.browser.find_element_by_id("login_button")
        button.click()
        profile = self.browser.find_element_by_id("profile")
        assert profile.text == "Mon compte"

        # visit the profile page
        profile.click()
        assert self.browser.title == "Mon profil"

        quiz_participated = self.browser.find_element_by_id("no_quiz_finished")
        assert quiz_participated.text == "Vous n'avez pas encore complété de quiz"
        
        show_created = self.browser.find_element_by_id("created")
        show_created.click()
        quiz_created = self.browser.find_element_by_id("no_quiz_created")
        assert quiz_created.text == "Vous n'avez pas encore crée de quiz"