"""Models and database functions for [video game] project."""

from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()  # Call methods on db instead of the entirety of the obj name.

###################################################
# MODEL DEFINITIONS

class User(db.Model)
	"""User of [video game] website."""

	__tablename__ = "users"  # SQLAlchemy dunder property that creates table with this name

	# Column names on left, type of data and properties on right.
	user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	username = db.Column(db.String(20), nullable=False)
	email = db.Column(db.String(64), nullable=False)
	password = db.Column(db.String(64), nullable=False)
	# Add optional "profile" columns before moving onto MVP 2.0

	def __repr__(self):
		"""Displays useful information when printed."""

		# <> brackets identify this as a class object at a glance
		return "<User user_id={}, username={}, email={}>".format(self.user_id,
																 self.username,
																 self.email)

class Game(db.Model)
	"""Game of [video game] website."""
