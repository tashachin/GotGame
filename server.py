"""[Video game] website."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
				   session)

from flask_debugtoolbar import DebugToolbarExtension

from model import (User, Game, Genre, VgGen, Difficulty, Comment, Tag,
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
	"""Displays results from homepage search-bar."""

	title = request.args.get('title')

	# .ilike ignores case when filtering
	game = Game.query.filter(Game.title.ilike('%' + title + '%')).first()

	return render_template('game_info.html', 
						   game=game)

@app.route('/login')
def show_login():
	"""Show login page."""

	return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
	"""Checks that user has entered correct password."""

	username = request.form.get('username')
	password = request.form.get('password')

	user = User.query.filter(User.username == username).first()

	if user and user.password == password:

		session['user_id'] = user.user_id
		flash("Logged in.")

		return redirect('/')
	
	else:
		flash("Username/password combination not recognized.")
		return redirect('/login')

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

	

@app.route('/game/<title>') # Game "profile" page
def show_game_profile():
	pass

@app.route('/new-user', methods=['POST'])
def validate_user():
	"""Checks if username/email are already in use. 
	If not, register new user."""

	username = request.form.get('username')
	email = request.form.get('email')
	password = request.form.get('password')

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

@app.route('/user/<username>')  # User profile page
def show_profile():
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