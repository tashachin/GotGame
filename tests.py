# import time

import unittest
import flask

import os

TEST_USERNAME = os.environ['TEST_USERNAME']
TEST_EMAIL = os.environ['TEST_EMAIL']
TEST_PASSWORD = os.environ['TEST_PASSWORD']

from server import app
from model import db, connect_to_db

from test_model import *

from selenium import webdriver

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

    def test_login(self):
        result = self.client.get('/login')
        self.assertIn('Username:', result.data)
        self.assertNotIn('Choose a password', result.data)

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


    def test_logout(self):
        """Checks for flash message when logging out."""

        result = self.client.get('/logout',
                                 follow_redirects=True)

        self.assertIn('Logged out.', result.data)


###################################################
# DATABASE ONLY TESTS

class GotGameDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to run before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, 'postgresql:///games')

    def tearDown(self):
        """Run at the end of every test."""

        db.session.close()


    def test_username_fail(self):
        """Checks that user cannot register with an existing username."""

        result = self.client.post('/new-user',
                                  data={'username': 'markiplier',
                                        'email': 'test@test.com',
                                        'password': 'lolol'},
                                  follow_redirects=True)

        self.assertIn('Sorry, that username is already in use.', result.data)


    def test_email_fail(self):
        """Checks that user cannot register with an existing email."""

        result = self.client.post('/new-user',
                                  data={'username': TEST_USERNAME,
                                        'email': 'markiplier@mark.com',
                                        'password': 'lolol'},
                                  follow_redirects=True)

        self.assertIn('Sorry, that email is already in use.', result.data)


    def test_login(self):
        """Checks for confirmation of successful login."""

        result = self.client.post('/login',
                                  data={'username': 'markiplier',
                                        'password': 'markiplier'},
                                  follow_redirects=True)

        self.assertIn('Logged in.', result.data)


    def test_login_fail(self):
        """Checks that user must input correct password."""

        result = self.client.post('/login',
                                  data={'username': 'markiplier',
                                        'password': 'tinyboxtim'},
                                  follow_redirects=True)

        self.assertIn('Username/password combination not recognized.', result.data)


    def test_title_search(self):
        """Checks results of a basic title search."""

        result = self.client.get('/search-results',
                                 query_string={'title': 'final fantasy'})

        self.assertIn('Crisis Core', result.data)


    def test_adv_search(self):
        """Tests the advanced search form page."""

        result = self.client.get('/adv-search')

        self.assertIn('Search by platform', result.data)
        self.assertIn('Action', result.data)  # Do the genres show up?


    def test_critic_filter(self):
        """Confirms that searching by (critic)score filters properly."""

        result = self.client.get('/adv-search-results', 
                                  query_string={'title': None,
                                                'critic_score': 10.0,
                                                'user_score': 0,
                                                'platform': None,
                                                'genres': None,})  # query_string is a GET specific keyword; data is the POST equivalent

        self.assertIn('Platform', result.data)  # Do the table headers render properly?
        self.assertIn('Checkered Flag', result.data)
        self.assertNotIn('Fury of The Hulk', result.data)  # This game scored a 1 and shouldn't show up

    def test_user_profile(self):
        """Checks username, reviews, # of reviews on user's profile page."""

        result = self.client.get('/user/1')

        self.assertIn('markiplier', result.data)  # Does the page display username?
        self.assertIn('To the Moon', result.data)  # Is the user's review on this page?
        self.assertIn('Number of games reviewed', result.data)
        self.assertIn('horror', result.data)  # Do his tags show up?


    def test_edit_profile(self):
        """Checks that the profile form displays correctly."""

        result = self.client.get('/edit-profile/1')

        self.assertIn('Max 500 characters', result.data)  # Bio chara-count limit

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

        connect_to_db(app, 'postgresql:///games')

    def tearDown(self):
        """Run at the end of every test."""

        db.session.close()


    def test_logged_in_navbar(self):
        """Checks that login status impacts navbar."""

        result = self.client.get('/')

        self.assertIn('Profile', result.data)
        self.assertIn('Logout', result.data)
        self.assertNotIn('Register', result.data)
        self.assertNotIn('Login', result.data)


    def test_game_info(self):
        """Checks if user has reviewed a game before."""

        result = self.client.get('/game/PC/The%20Binding%20of%20Isaac:%20Rebirth')

        self.assertIn('Looking forward to future add-ons.', result.data)  # Does test review show up?
        self.assertIn('rec', result.data)
        self.assertIn('game_id', result.data)


###################################################
# ADDING TO DATABASE

class AddToDatabase(unittest.TestCase):
    """Create empty database to test features that add data."""

    def setUp(self):

        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, 'postgresql:///testdb')
        db.create_all()

        user = User(username='markiplier',
                    email='markiplier@mark.com',
                    password='markiplier',
                    birthday='1989-06-28',
                    location='LA',
                    bio='Hello, everybody! My name is Markiplier.',
                    fave_game="Sid Meier's Civilization V")

        db.session.add(user)
        db.session.commit()

    def tearDown(self):

        db.session.remove()
        db.drop_all()


    def test_registration(self):
        """Checks for notification upon successful registration."""

        result = self.client.post('/new-user',
                                  data={'username': TEST_USERNAME,
                                        'email': TEST_EMAIL,
                                        'password': TEST_PASSWORD},
                                  follow_redirects=True)

        self.assertIn('You&#39;ve been registered. Game on!', result.data)
        self.assertIn('Username:', result.data)
        self.assertNotIn('Email', result.data)


###################################################
# SELENIUM TESTS


class BrowserTests(unittest.TestCase):
    """Test JSON and front-end functionality."""

    def setUp(self):

        self.browser = webdriver.Chrome()


    def tearDown(self):
        self.browser.quit()


    def test_title(self):
        self.browser.get('http://localhost:5000/')
        self.assertEqual(self.browser.title, 'Got Game?')


###################################################
# HELPER FUNCTIONS

if __name__ == "__main__":
    unittest.main()
