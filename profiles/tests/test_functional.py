from django.contrib.staticfiles.testing import StaticLiveServerTestCase

import pytest

import selenium


def TestProfile(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_profile_page(self):
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