import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

###################################################
# SELENIUM TESTS

class BrowserTests(unittest.TestCase):
    """Test JSON and front-end functionality."""

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 10)  # Used for following redirects


    def tearDown(self):
        self.browser.quit()


    def test_title(self):
        self.browser.get('http://localhost:5000/')
        self.assertEqual(self.browser.title, 'Got Game?')


    def test_login(self):
        self.browser.get('http://localhost:5000/login')

        username = self.browser.find_element_by_id('user')
        username.send_keys('markiplier')

        password = self.browser.find_element_by_id('password')
        password.send_keys('markiplier')

        btn = self.browser.find_element_by_id('submit')
        btn.click()

        self.wait.until(EC.url_to_be('http://localhost:5000/'))
        self.assertIn('Logged in.', self.browser.page_source)
    

    def test_adv_search(self):
        self.browser.get('http://localhost:5000/adv-search')

        user_score = self.browser.find_element_by_id('user_scores')
        user_score.send_keys('5')

        btn = self.browser.find_element_by_id('submit')
        btn.click()

        self.wait.until(EC.url_to_be('http://localhost:5000/adv-search-results?critic_score=&user_scores=5'))
        self.assertIn('Left 4 Dead 2', self.browser.page_source)
        self.assertIn('Score (IGN)', self.browser.page_source)


    def test_userflow(self):
        self.browser.get('http://localhost:5000/user/1')
        self.assertIn('Hello, everybody! My name is Markiplier.', self.browser.page_source)

        link = self.browser.find_element_by_id('review-1')
        link.click()

        self.wait.until(EC.url_to_be('http://localhost:5000/game/PC/Dead%20Island'))
        self.assertIn('zombie-infested island', self.browser.page_source)

        btn = self.browser.find_element_by_id('open-add-tag-modal')
        btn.click()

        element = self.browser.find_element_by_id('tag-field')
        html = self.browser.execute_script('return arguments[0].innerHTML;', element)

        self.assertIn('fave', html)


if __name__ == "__main__":
    unittest.main()
