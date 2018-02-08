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

###################################################
# ADD TO DATABASE

def create_user(username, email, password):
	"""Takes info from '/register' and submits user to database."""
	new_user = User(username=username,
					email=email,
					password=password)
	db.session.add(new_user)
	db.session.commit()

def create_review(game_id, review):
	"""Takes info from '/game/<title>' and submits review to database."""

	user_id = session['user_id']

	new_review = Review(user_id=user_id,
						game_id=game_id,
						review=review)

	db.session.add(new_review)
	db.session.commit()

	# return redirect('/search-results?title=' + ) FIX ME!!!!!!

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
		return render_template('game_info.html', 
						   	   game=game,
						   	   review=None)  # Come back to this later!

	else:
		flash("Oops! Our database didn't return any results.")
		return redirect('/')

def get_title(title):  # Takes in request.args.get() value
	"""Returns a query by title."""

	query = Game.query.filter(Game.title.ilike('%' + title + '%')).limit(25).all()
	
	return query


def get_title_and_platform(title, platform):
	"""Returns all games containing 'title' for a specific platform."""

	query = Game.query.filter(Game.title.ilike('%' + title + '%'), Game.platform.ilike('%' + platform + '%')).limit(25).all()

	return query


def get_score(score):
	"""Returns a query by score."""

	query = Game.query.filter(Game.critic_score >= score).limit(25).all()

	return query


def get_platform(platform):
	"""Returns a query by platform."""

	query = Game.query.filter(Game.platform.ilike('%' + platform + '%')).limit(25).all()

	return query


def get_score_and_platform(score, platform):
	"""Returns a query that filters by a certain score and platform."""

	query = Game.query.filter(Game.critic_score >= score, Game.platform.ilike('%' + platform + '%')).limit(25).all()

	return query