"""Contains helper functions to be used in server."""

from model import *

###################################################
# USER INPUT

def create_user(username, email, password):
	"""Takes info from '/register' and submits user to database."""
	new_user = User(username=username,
					email=email,
					password=password)
	db.session.add(new_user)
	db.session.commit()

###################################################
# QUERIES
def get_title(title):  # Takes in request.args.get() value
	"""Returns a query by title."""

	query = Game.query.filter(Game.title.ilike('%' + title + '%')).limit(25).all()
	
	return query


def get_title_and_platform(title, platform):
	"""Returns all games containing 'title' for a specific platform."""

	query = Game.query.filter((Game.title.ilike('%' + title + '%')), (Game.platform.ilike('%' + platform + '%'))).limit(25).all()

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

	query = Game.query.filter((Game.critic_score >= score), (Game.platform.ilike('%' + platform + '%'))).limit(25).all()

	return query