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
		return redirect('/')


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

	if check_login_status():
		review = Review.query.filter(Review.game_id == game.game_id and Review.user_id == user_id).first()  # Display user's previous review in Jinja.

		return review

	else:
		review = None  # Display form in Jinja to add a review.

		return review

###################################################
# ADD TO DATABASE

def create_user(username, email, password):
	"""Takes info from '/register' and submits user to database."""
	new_user = User(username=username,
					email=email,
					password=password)

def create_review(game_id, review):
	"""Takes info from '/game/<title>' and submits review to database."""

	user_id = session['user_id']

	new_review = Review(user_id=user_id,
						game_id=game_id,
						review=review)

def update_user_score(game_id, user_score):
	"""Takes info from '/game/<title>' and updates game's score."""

	game = Game.query.filter(Game.game_id == game_id).first()

	game.user_score = user_score

	db.session.commit()

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

def get_one_title(title):
	"""Displays results from homepage search-bar."""

	# .ilike ignores case when filtering
	game = Game.query.filter(Game.title.ilike('%' + title + '%')).first()

	if game:
		return game

	else:
		flash("Oops! Our database didn't return any results.")
		return redirect('/')

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