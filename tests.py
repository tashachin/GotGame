import unittest
import flask

from server import app
from model import db, connect_to_db

from test_model import *

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

	def test_adv_search_access(self):
		"""Checks that flash message displays when user tries to see results
		without entering any search queries."""

		result = self.client.get('/adv-search-results',
								 follow_redirects=True)

		self.assertIn('Uh-oh! Something went wrong.', result.data)

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

	def test_login_fail(self):
		"""Checks that user cannot register with an existing username."""
		result = self.client.post('/new-user',
								  data={'username': 'ffluvr93',
								  		'email': 'test@test.com',
								  		'password': 'lolol'},
								  follow_redirects=True)

		self.assertIn('Sorry, that username is already in use.', result.data)

	# *Testing current iteration. Not how I want actual search to work.
	def test_basic_search(self):  
		"""Checks that a game from the database shows up after searching on homepage."""

		result = self.client.get('/search-results?title=best')

		self.assertIn('Best Game Ever', result.data)

	# Currently not working
	def test_adv_search(self):
		"""Confirms that searching by (critic)score filters properly."""

		result = self.client.get('/adv-search-results', 
								  query_string={'title': None,
								  				'score': 5.0,
								  				'platform': None})  # query_string is a GET specific keyword; data is the POST equivalent

		self.assertIn('Best Game Ever', result.data)
		self.assertIn('So-So Game', result.data)
		self.assertNotIn('Bargain Bin Game', result.data)

if __name__ == "__main__":
	unittest.main()
