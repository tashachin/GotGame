"""Contains helper functions to be used in server."""
from flask import (Flask, render_template, redirect, request, flash,
				   session)

from model import *

###################################################
# VALIDATION

def check_credentials(username, password):
	"""Logic for checking login credentials."""

	user = User.query.filter(User.username == username).first()

	if user and user.password == password:

		session['user_id'] = user.user_id
		flash("Logged in.")

		return redirect('/')
	
	else:
		flash("Username/password combination not recognized.")
		return redirect('/login')

def process_registration(username, email, password):
	"""Directs user trying to register, depending on user's input."""

	email_check = User.query.filter(User.email == email).first()
	username_check = User.query.filter(User.username == username).first()

	if email_check:
		flash("Sorry, that email is already in use.")
		return redirect('/register')

	elif username_check:
		flash("Sorry, that username is already in use.")
		return redirect('/register')

	else:
		create_user(username, email, password)

		flash("You've been registered. Game on!")
		return redirect('/login')


def check_login_status():
	"""Checks to see if user is logged in."""

	if session.get('user_id'):
		user_id = session['user_id']

		return user_id

	else:
		user_id = None
		
		return user_id


def check_review_status(game):
	"""Checks to see if user is logged in and if game has been reviewed before."""

	user_id = check_login_status()

	if user_id:
		review = Review.query.filter(Review.user_id == user_id, Review.game_id == game.game_id).first()
		return review

	else:
		review = None  # Display form in Jinja to add a review.

		return review


def handle_invalid_search(game):
	"""Handles logic for redirecting user when game does not exist in database."""

	if game:
		game_id = game.game_id

		user_status = check_login_status()
		review = check_review_status(game)
		
		user_id = session.get('user_id')

		reviews = retrieve_game_reviews(user_id, game_id)

		vg_genres = retrieve_genres(game_id)

		return render_template('game_info.html',
							   game=game,
							   user_id=user_id,
							   user_status=user_status,
							   review=review,
							   reviews=reviews,
							   vg_genres=vg_genres)
	else:
		flash("Oops! Our database didn't return any results.")
		return redirect('/')

###################################################
# ADD TO DATABASE

def create_user(username, email, password):
	"""Takes info from '/register' and submits user to database."""
	new_user = User(username=username,
					email=email,
					password=password)

	db.session.add(new_user)
	db.session.commit()

def create_review(game_id, review, user_score):
	"""Takes info from '/game/<title>' and submits review to database."""

	user_id = session['user_id']

	new_review = Review(user_id=user_id,
						game_id=game_id,
						user_score=user_score,
						review=review)

	db.session.add(new_review)
	db.session.commit()

def update_review(game_id, review_text, user_score):
	"""Takes info from '/game/<title>' and updates game's score."""

	user_id = session['user_id']

	review = Review.query.filter(Review.user_id == user_id, Review.game_id == game_id).one()

	review.review = review_text
	review.user_score = user_score

	db.session.commit()


def aggregate_score():
	"""Update user score anytime a user adds or edits a review."""

	reviews = Review.query.filter(Review.game.game_id == game_id).all()



	pass

###################################################
# SEARCH FILTERING

def apply_filters(title, score, platform):
	"""Checks how to query database based on user's filters."""

	if title:
			if title and platform:

				games = get_title_and_platform(title, platform)
				return render_template('adv_search_results.html',
									   games=games)

			else:
				games = get_title(title)
				return render_template('adv_search_results.html',
								   	   games=games)
	else:
		if score and platform:
			games = get_score_and_platform(score, platform)

			return render_template('adv_search_results.html',
								   games=games)
		elif score:
			games = get_score(score)

			return render_template('adv_search_results.html',
								   games=games)

		elif platform:
			games = get_platform(platform)

			return render_template('adv_search_results.html',
								   games=games)
		else:
			flash("Uh-oh! Something went wrong.")
			return redirect('/adv-search')

###################################################
# QUERIES

def retrieve_user(user_id):
	"""Gets user info from '/user/<user_id>'"""

	user = User.query.filter(User.user_id == user_id).one()

	return user

def retrieve_user_reviews(user_id):

	query = Review.query.filter(Review.user_id == user_id)

	num_reviews = query.count()
	reviews = query.limit(15)

	return num_reviews, reviews


def retrieve_game_reviews(user_id, game_id):
	"""Returns all reviews for a specific game from OTHER users."""

	reviews = Review.query.filter(Review.game_id == game_id, Review.user_id != user_id).limit(10).all()

	return reviews


def retrieve_genres(game_id):
	"""Returns all the genres associated with a specific game."""

	vg_genres = VgGen.query.filter(VgGen.game_id == game_id).all()

	return vg_genres


def get_one_title(title):
	"""Displays results from homepage search-bar."""

	# .ilike ignores case when filtering
	game = Game.query.filter(Game.title.ilike('%' + title + '%')).first()

	if game:
		return game


def get_title(title):  # Takes in request.args.get() value
	"""Returns a query by title."""

	query = Game.query.filter(Game.title.ilike('%' + title + '%')).all()
	
	return query


def get_title_and_platform(title, platform):
	"""Returns all games containing 'title' for a specific platform."""

	query = Game.query.filter(Game.title.ilike('%' + title + '%'), Game.platform.ilike('%' + platform + '%')).all()

	return query


def get_score(score):
	"""Returns a query by score."""

	query = Game.query.filter(Game.critic_score >= score).all()

	return query


def get_platform(platform):
	"""Returns a query by platform."""

	query = Game.query.filter(Game.platform.ilike('%' + platform + '%')).all()

	return query


def get_score_and_platform(score, platform):
	"""Returns a query that filters by a certain score and platform."""

	query = Game.query.filter(Game.critic_score >= score, Game.platform.ilike('%' + platform + '%')).all()

	return query


def average_user_score():
	"""Calculates the average user score based on all user scores."""

	game = Game.query.filter(Game.title == title, Game.platform == platform).first()



