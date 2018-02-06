"""Models and database functions for [video game] project."""

from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()  # Call methods on db instead of the entirety of the obj name.

###################################################
# MODEL DEFINITIONS

class User(db.Model):
	"""User of [video game] website."""

	__tablename__ = "users"  # SQLAlchemy dunder property that creates table with this name

	# Column names on left, type of data and properties on right.
	user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	username = db.Column(db.String(20), nullable=False)
	email = db.Column(db.String(64), nullable=False)
	password = db.Column(db.String(64), nullable=False)
	# Add optional "profile" columns before moving onto MVP 2.0

	def __repr__(self):
		"""Displays useful information about user when printed."""

		# <> brackets identify this as a class object at a glance
		return "<User user_id={}, username={}, email={}>".format(self.user_id,
																 self.username,
																 self.email)

class Game(db.Model):
	"""Game of [video game] website."""

	__tablename__ = "games"

	game_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	title = db.Column(db.String(256), nullable=False)
	system = db.Column(db.String(25), nullable=True)  # What console version is this game?
	critic_score = db.Column(db.Integer, nullable=False)
	user_score = db.Column(db.Integer, nullable=True)

	def __repr__(self):
		"""Displays useful information about game when printed."""

		return "<Game game_id={}, title={}>".format(self.game_id,
													self.title)

class Genre(db.Model):
	"""List of possible genres to label a game.""" 

	__tablename__ = "genres"

	genre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	genre_type = db.Column(db.String(25), nullable=False)

	def __repr__(self):
		"""Displays useful information about genre when printed."""

		return "<Genre genre_id={}, genre_type={}>".format(self.genre_id,
															 self.genre_type)

class VgGen(db.Model):
	"""Genre(s) of a game."""

	__tablename__ = "vg_genres"  # Check naming conventions for two-word tables.

	vg_genre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'))
	genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id'))

	# Two-way access between game and genre info:
	# Can query what genres a game belongs to
	game = db.relationship("Game", backref=db.backref("vg_genres",
													  order_by=vg_genre_id))

	genre = db.relationship("Genre", backref=db.backref("vg_genres",
													   order_by=vg_genre_id))
	def __repr__(self):
		"""Displays useful information about game's genres when printed."""

		# Is it possible to customize repr to print all genre_ids?
		return "<VgGen vg_genre_id={}, title={}, genres={}>".format(self.vg_genre_id,
																	  self.game.title,
																	  self.genre.genre_type)

class Difficulty(db.Model):
	"""Difficulty of a game."""

	__tablename__ = "difficulty"

	difficulty_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'))
	level = db.Column(db.Integer, nullable=False)  # Numerical representation of how hard a game is
	
	game = db.relationship("Game", backref=db.backref("difficulty",
													  order_by=difficulty_id))

	def __repr__(self):
		"""Displays useful information about difficulty when printed."""

		return "<Difficulty difficulty_id={}, game_id={}, game={}, level={}>".format(self.difficulty_id,
																						  self.game.game_id,
																						  self.game.title,
																						  self.level)  # Is this intuitive?

class Comment(db.Model):
	"""Comment of a user."""

	__tablename__ = "comments"

	comment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'))
	comment = db.Column(db.String(1000), nullable=False)  # A little over two paragraphs?
	# Implement thread_id later if creating forum/chain of comments (MVP 3.0)

	user = db.relationship("User", backref=db.backref("comments",
													  order_by=comment_id))
	game = db.relationship("Game", backref=db.backref("comments",
													  order_by=comment_id))


class Tag(db.Model):
	"""A user-generated tag to label a game."""

	__tablename__ = "tags"

	tag_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id')) # Who created the tag?
	game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'))  # Which game is the tag associated with?
	tag = db.Column(db.String(30), nullable=False)

class TagCategory(db.Model):
	"""A category that a tag belongs to."""

	__tablename__ = "tag_cats"

	tag_cat_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	tag_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id'))
	# Which aspect of gaming is this tag for?
	# (i.e. 'genre', '# of players', 'gameplay')
	category = db.Column(db.String(30), nullable=False)

	tag = db.relationship("Tag", backref=db.backref("tag_cats",
													order_by=tag_cat_id))

###################################################
# HELPER functions

def connect_to_db(app):
	"""Connect the database to Flask app."""

	# Configure to use PostgreSQL database
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///games'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.app = app
	db.init_app(app)

if __name__ == "__main__":

	from server import app
	connect_to_db(app)
	print "Connected to DB."  # Confirm on console that server is up.