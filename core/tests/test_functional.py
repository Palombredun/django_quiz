from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from time import sleep


class TestHome(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_navigate_home(self):
        """
		GIVEN a user who wants to visit the website Fast & Quizzy
		WHEN the user launches Firefox to access the website
		THEN assert that he has the good page and content
		"""
        self.browser.get(self.live_server_url)

        heading2 = self.browser.find_element_by_tag_name("h2")
        profile = self.browser.find_element_by_name("profile")

        assert self.browser.title == "Fast & Quizy"
        assert heading2.text == "Derniers quiz crées"
        assert profile.t is None
