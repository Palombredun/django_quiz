from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from time import sleep

class TestAccount(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_create_account_login_and_visite_profile(self):
        """
        GIVEN a new user who wants to participate to quizzes
        WHEN he creates an account
        THEN assert he can login, logout, and visit his profile
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

        # assert we are redirected to the home page, and that the header is updated
        assert self.browser.title == "Fast & Quizy"
        profile = self.browser.find_element_by_id("profile")
        assert profile.text == "Mon compte"

        # logout
        logout_link = self.browser.find_element_by_id("logout")
        logout_link.click()
        assert self.browser.title == "Fast & Quizy"