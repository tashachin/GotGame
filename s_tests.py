import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

desired_cap = {
'browserName': 'iPhone',
'device': 'iPhone 7',
'realMobile': 'true',
'os_version': '10.3'
}

class BrowserTests(unittest.TestCase):

    def setUp():
        driver = webdriver.Chrome()
        driver.get("localhost:5000/")

    def tearDown():
        print 'The /welcome route loaded successfully for the user'
        driver.quit()

    def test_homepage():
        driver.get("localhost:5000/")
        assert "Got Game?" in driver.title
