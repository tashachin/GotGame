import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

###################################################
# SELENIUM TESTS

class BrowserTests(unittest.TestCase):
    """Test JSON and front-end functionality."""

    def setUp(self):
        self.browser = webdriver.Chrome()


    def tearDown(self):
        print "Testing"
        self.browser.quit()



    def test_title(self):
        self.browser.get('http://localhost:5000/')
        self.assertEqual(self.browser.title, 'Got Game?')


if __name__ == "__main__":
    unittest.main()
