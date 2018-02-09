"""[Video game] website."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
				   session, jsonify)

from flask_debugtoolbar import DebugToolbarExtension

from model import (User, Game, Genre, VgGen, Difficulty, Review, Tag,
				   TagCategory, VgTag)

from model import db, connect_to_db

from helper import *

app = Flask(__name__)

app.secret_key = "Placeholder"  # Look into .secret_key later

app.jinja_env.undefined = StrictUndefined  # Provides better error message support

###################################################
# APP ROUTES

@app.route('/')
def homepage():
	"""Displays homepage."""

	return render_template('homepage.html')

@app.route('/search-results') 
def show_basic_results():  
	"""A fun quick-search for the homepage."""

	title = request.args.get('title')

	game = get_one_title(title)

	review = check_review_status(game)

	return render_template('game_info.html',
						   game=game,
						   review=review)

@app.route('/login')
def show_login():
	"""Show login page."""

	return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
	"""Checks that user has entered correct password."""

	username = request.form.get('username')
	password = request.form.get('password')

	return check_credentials(username, password)

@app.route('/logout')
def logout():
	"""Logs user out of site."""

	session.clear()
	flash("Logged out.")
	return redirect('/')

@app.route('/register')
def register():
	"""Show new user registration form."""

	return render_template('register.html')

@app.route('/adv-search')
def advanced_search():
	"""Displays advanced search options."""
	
	return render_template('advanced_search.html')

@app.route('/adv-search-results')
def show_advanced_results():
	"""Displays results after filters get applied."""

	title = request.args.get('title')
	score = request.args.get('score')
	platform = request.args.get('platform')

	return apply_filters(title, score, platform)

@app.route('/user/<username>')  # User profile page
def show_profile():
	pass

@app.route('/game/<title>') # Game "profile" page
def show_game_profile(title):

	# take string title and query db, then feed obj back into jinja
	pass

@app.route('/new-user', methods=['POST'])
def validate_user():
	"""Checks if username/email are already in use. 
	If not, register new user."""

	username = request.form.get('username')
	email = request.form.get('email')
	password = request.form.get('password')

	return process_registration(username, email, password)  # In helper.py

@app.route('/new-review.json', methods=['POST'])  # In a .json route, 'form data' needs to be passed as second arg
def get_review_info():
	"""Return info about a game as JSON"""

	# This will not work unless 'form data' gets passed through
	game_id = request.form.get('game_id')
	user_score = request.form.get('user_score')
	review = request.form.get('review')

	update_user_score(game_id, user_score)
	create_review(game_id, review)

	review_info = {
		"game_id": game_id,
		"user_score": user_score,
		"review": review
	}

	print """NEW REVIEW: {} {}""".format(game_id, review)
	return jsonify(review_info)

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