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

	def test_adv_search_access(self):  # Will probably need a code review for this one
		"""Checks that flash message displays when user tries to see results
		without entering any search queries."""

		pass

class GotGameDatabase(unittest.TestCase)
	"""Flask tests that use the database."""

	def setUp(self):
		"""Stuff to run before every test."""

		self.client = app.test_client()
		app.config['TESTING'] = True

		connect_to_db(app, 'postgresql:///testdb')

		db.create_all()
		example_data()

if __name__ == "__main__":
	unittest.main()