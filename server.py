"""[Video game] website."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
				   session)

from flask_debugtoolbar import DebugToolbarExtension

from model import (User, Game, Genre, VgGen, Difficulty, Comment, Tag,
				   TagCategory, VgTag)
from model import connect_to_db

app = Flask(__name__)

app.secret_key = "Placeholder"  # Look into .secret_key later

app.jinja_env.undefined = StrictUndefined  # Provides better error message support

###################################################
# APP ROUTES

@app.route('/')
def homepage():
	"""Displays homepage."""

	return render_template('homepage.html')

@app.route('/advanced-search')
def advanced_search():
	"""Displays advanced search options."""
	
	return render_template('advanced_search.html')

@app.route('/search-results')  # *Change URL to search query (?=userinput) | Shows search results
# Splitting up search bar leads for debugging
# May consider merging after testing

# def show_basic_results():  
# 	"""Displays results from homepage search-bar."""

# 	title = request.args.get('title')

# 	# .ilike ignores case when filtering
# 	game = Game.query.filter(Game.title.ilike('%' + title + '%')).first()

# 	return render_template('game_info.html', 
# 						   game=game)

def show_advanced_results():
	"""Displays results after filters get applied."""

	title = request.args.get('title')
	score = request.args.get('score')
	platform = request.args.get('platform')

	if title:
		titles = get_title(title)

		return render_template('test.html',
							   titles=titles)

	else:
		pass
	# 	if score and platform:
	# 		scores = get_score(score)

	# 	if platform:
	# 		platform = get_platform(platform)

	# # Currently, this function will only work if all filters are on...
	# # May need to break this up into smaller functions
	# return render_template('test.html',
	# 					   title_query=title_query,
	# 					   score_query=score_query,
	# 					   platform_query=platform_query)  # Ultimately, I want to return potential games, not the entire query results

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

def get_title(title):  # Takes in request.args.get() value
	"""Returns a query by title."""

	query = Game.query.filter(Game.title.ilike('%' + title + '%')).limit(25).all()
	
	return query

def get_score(score):
	"""Returns a query by score."""

	query = Game.query.filter(Game.critic_score >= score).limit(25).all()

	return query

def get_platform(platform):
	"""Returns a query by platform."""

	query = Game.query.filter(Game.platform.ilike('%' + platform + '%')).limit(25).all()

	return query

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