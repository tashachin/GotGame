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

	return handle_invalid_search(game)  # Had to handle invalid search input

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


@app.route('/genre-search')
def genre_search():
	"""Displays checkbox options for searching by genre."""

	genres = Genre.query.all()

	return render_template('genre_search.html',
						   genres=genres)


@app.route('/genre-search-results')
def show_genre_results():
	"""Displays results after searching by genre."""

	genre_ids = request.args.getlist('genre')

	vg_genres = VgGen.query.filter(VgGen.genre_id.in_(genre_ids)).all()

	return render_template('genre_search_results.html',
						   vg_genres=vg_genres)


@app.route('/user/<user_id>')  # User profile page
def show_profile(user_id):

	user = retrieve_user(user_id)
	num_reviews, reviews = retrieve_user_reviews(user_id)

	return render_template('user_profile.html',
						   user=user,
						   num_reviews=num_reviews,
						   reviews=reviews)

@app.route('/game/<platform>/<title>') # Game "profile" page
def show_game_profile(platform, title):
	
	game = Game.query.filter(Game.title == title, Game.platform == platform).one()
	game_id = game.game_id

	vg_genres = retrieve_genres(game_id)
	user_status = check_login_status()
	review = check_review_status(game)

	if check_login_status():
		user_id = check_login_status()
		reviews = retrieve_game_reviews(user_id, game.game_id)

	else:
		reviews = None

	return render_template('game_info.html',
							 game=game,
							 user_status=user_status,
							 review=review,
							 reviews=reviews,
							 vg_genres=vg_genres)

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
	"""Return info about a game review as JSON."""

	# This will not work unless 'form data' gets passed through
	user_score = request.form.get('user_score')
	game_id = request.form.get('game_id')
	review = request.form.get('review')

	user_id = session['user_id']

	create_review(game_id, review, user_score)

	review_info = {
		"game_id": game_id,
		"user_score": user_score,
		"review": review,
	}

	print """<NEW REVIEW: game_id={}, user_score={}, review={}>""".format(game_id, 
																		  user_score, 
																		  review)
	return jsonify(review_info)


@app.route('/edit-review.json', methods=['POST'])
def edit_review():
	"""Return info about user updating a game review as JSON."""

	user_score = request.form.get('edit_user_score')
	game_id = request.form.get('game_id')
	review_text = request.form.get('edit_review')

	user_id = session['user_id']

	update_review(game_id, review_text, user_score)

	review_info = {
		"game_id": game_id,
		"user_score": user_score,
		"review_text": review_text,
	}

	print """<UPDATED REVIEW: game_id={}, user_score={}, review={}>""".format(game_id, 
																			  user_score, 
																			  review_text)
	return jsonify(review_info)


@app.route('/')
def get_tag_info():
	"""Return info about a user's game tag as JSON."""
	pass

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