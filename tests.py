import unittest
import flask

from server import app
from model import db, connect_to_db

from test_model import *

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

###################################################
# BASIC TESTS

class GotGameTests(unittest.TestCase):
	"""Tests for my 'Got Game?' site."""

	def setUp(self):
		self.client = app.test_client()
		app.config['TESTING'] = True


	def test_homepage(self):
		result = self.client.get('/')
		self.assertIn('Advanced search', result.data)


	def test_registration(self):
		result = self.client.get('/register')
		self.assertIn('Choose a password', result.data)


	def test_adv_search(self):
		result = self.client.get('/adv-search')
		self.assertIn('Search by platform', result.data)


	def test_adv_search_access(self):
		"""Checks that flash message displays when user tries to see results
		without entering any search queries."""

		result = self.client.get('/search-results',
								 follow_redirects=True)

		self.assertIn('Uh-oh! Something went wrong.', result.data)

###################################################
# LOGGED IN TESTS

class GotGameLoggedIn(unittest.TestCase):
	"""Tests that require user to be logged in."""

	def setUp(self):
		app.config['TESTING'] = True
		app.config['SECRET_KEY'] = 'key'
		self.client = app.test_client()

		with self.client as c:
			with c.session_transaction() as sess:
				sess['user_id'] = 1


	def test_navbar(self):
		"""Checks that navbar displays proper links."""

		result = self.client.get('/')

		self.assertIn('<a href="/user/1">Profile</a>', result.data)
		self.assertNotIn('Login', result.data)

###################################################
# DATABASE ONLY TESTS

class GotGameDatabase(unittest.TestCase):
	"""Flask tests that use the database."""

	def setUp(self):
		"""Stuff to run before every test."""

		self.client = app.test_client()
		app.config['TESTING'] = True

		connect_to_db(app, 'postgresql:///testdb')

		db.create_all()
		example_data()


	def tearDown(self):
		"""Run at the end of every test."""

		db.session.close()
		db.drop_all()


	def test_logout(self):
		"""Checks for flash message when logging out."""

		result = self.client.get('/logout',
								 follow_redirects=True)

		self.assertIn('Logged out.', result.data)


	def test_login_fail(self):
		"""Checks that user cannot register with an existing username."""

		result = self.client.post('/new-user',
								  data={'username': 'ffluvr93',
								  		'email': 'test@test.com',
								  		'password': 'lolol'},
								  follow_redirects=True)

		self.assertIn('Sorry, that username is already in use.', result.data)


	def test_adv_search(self):
		"""Confirms that searching by (critic)score filters properly."""

		result = self.client.get('/search-results', 
								  query_string={'title': None,
								  				'critic_score': 5.0,
								  				'user_score': 0,
								  				'platform': None,
								  				'genres': None,})  # query_string is a GET specific keyword; data is the POST equivalent

		self.assertIn('Best Game Ever', result.data)
		self.assertIn('So-So Game', result.data)
		self.assertNotIn('Bargain Bin Game', result.data)


	def test_user_profile(self):
		"""Checks username, reviews, # of reviews on user's profile page."""

		result = self.client.get('/user/1')

		self.assertIn('ffluvr93', result.data)  # Does the page display username?
		self.assertIn('Best Game Ever', result.data)  # Is the user's review on this page?
		self.assertIn('Number of games reviewed', result.data)


###################################################
# LOGGED IN & DATABASE TESTS

class DatabaseAndLoggedIn(unittest.TestCase):
	"""Flask tests that require a user logged in before communicating with database."""

	def setUp(self):
		app.config['TESTING'] = True
		app.config['SECRET_KEY'] = 'key'
		self.client = app.test_client()

		with self.client as c:
			with c.session_transaction() as sess:
				sess['user_id'] = 1

		connect_to_db(app, 'postgresql:///testdb')

		db.create_all()
		example_data()


	def tearDown(self):
		"""Run at the end of every test."""

		db.session.close()
		db.drop_all()


	def test_game_info(self):
		"""Checks if user has reviewed a game before."""

		result = self.client.get('/game/Xbox%20360/Best%20Game%20Ever')

		self.assertIn('Literally the best game ever.', result.data)  # Does test review show up?
		self.assertIn('Update your review', result.data)
		self.assertNotIn('Review Best Game Ever', result.data)


###################################################
# SELENIUM TESTS

class Browser(unittest.TestCase):
	"""Selenium automated browser tests."""

	def setUp(self):
		self.browser = webdriver.Chrome()

	def tearDown(self):
        self.browser.quit()

    def test_title(self):
        self.browser.get('http://localhost:5000')
        self.assertEqual(self.browser.title, 'Got Game?')

    def test_login(self):
        # self.browser.get('http://localhost:5000/login')

        # username = self.browser.find_element_by_id('user')
        # username.send_keys('markiplier')
        # password = self.browser.find_element_by_id('password')
        # password.send_keys('markiplier')
        # submit = self.browser.find_element_by_id('submit')
        # submit.click()

        # https://stackoverflow.com/a/47353551
        
        pass

###################################################
# HELPER FUNCTIONS

if __name__ == "__main__":
	unittest.main()
