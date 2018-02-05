"""[Video game] website."""

from jinja2 import StrictUndefined  # Provides better error message support.

from flask import (Flask, render_template, redirect, request, flash,
				   session)

from flask_debugtoolbar import DebugToolbarExtension

# from model import (all class-tables), connect_to_db, db 

app = Flask(__name__)

app.secret_key = "Placeholder"  # Look into .secret_key later

app.jinja_env.undefined = StrictUndefined

###################################################
# APP ROUTES

@app.route('/')
def homepage():
	"""Displays homepage."""
	pass

###################################################
# DEBUGGING

if __name__ == "__main__":
	# Must be initialized as True when invoking DebugToolbarExtension
	app.debug = True
	# Prevents templates, etc. aren't cached during debug mode
	app.jinja_env.auto_reload = app.debug

	conect_to_db(app)

	DebugToolbarExtension(app)

	app.run(port=500, host='0.0.0.0')