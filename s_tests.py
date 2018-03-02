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
        

if __name__ == "__main__":
    unittest.main()
