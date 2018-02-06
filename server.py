"""[Video game] website."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
				   session)

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db  # don't forget other stuff

app = Flask(__name__)

app.secret_key = "Placeholder"  # Look into .secret_key later

app.jinja_env.undefined = StrictUndefined  # Provides better error message support

###################################################
# APP ROUTES

@app.route('/')
def homepage():
	"""Displays homepage."""

	return render_template('homepage.html')

@app.route('/advanced-search')  # Show search bar with filtering ability
def advance_search():
	pass

@app.route('/search-results')  # *Change URL to search query (?=userinput) | Shows search results
def show_results():
	pass

@app.route('/game/<title>') # Game "profile" page
def show_game_profile():
	pass

@app.route('/registration-form')  # Display reg-form
def show_reg_form():
	pass

@app.route('/new-user', methods=['POST'])  # New user creation (add to database)
def create_user():
	pass

def validate_user():
	pass

@app.route('/user/<username>')  # User profile page
def show_profile():
	pass

###################################################
# FUNCTIONS

###################################################
# DEBUGGING

if __name__ == "__main__":
	# Must be initialized as True when invoking DebugToolbarExtension
	app.debug = True
	# Prevents templates, etc. aren't cached during debug mode
	app.jinja_env.auto_reload = app.debug

	connect_to_db(app)

	DebugToolbarExtension(app)

	app.run(port=5000, host='0.0.0.0')