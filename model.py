"""Models and database functions for [video game] project."""
from flask_sqlalchemy import SQLAlchemy 

from datetime import datetime

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
	joined_at = db.Column(db.Date, default=datetime.utcnow)
	birthday = db.Column(db.Date)
	location = db.Column(db.String(50))
	bio = db.Column(db.String(500))
	fave_game = db.column(db.String(256))

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
	platform = db.Column(db.String(25), nullable=True)  # What console version is this game?
	critic_score = db.Column(db.Float, nullable=False)
	aggregate_score = db.Column(db.Float, nullable=True)

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

class Difficulty(db.Model):  # Not using this anymore(?)
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

class Review(db.Model):
	"""Review of a user."""

	__tablename__ = "reviews"

	review_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'))
	user_score = db.Column(db.Integer, nullable=False)
	review = db.Column(db.String(1000), nullable=False)  

	user = db.relationship("User", backref=db.backref("reviews",
													  order_by=review_id))
	game = db.relationship("Game", backref=db.backref("reviews",
													  order_by=review_id))

	def __repr__(self):
		"""Displays useful info about review when printed."""

		return "<Review review_id={}, user={}, game={}>".format(self.review_id,
																  self.user.username,
																  self.game.title)

class Tag(db.Model):
	"""A user-generated tag to label a game."""

	__tablename__ = "tags"

	tag_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id')) # Who created the tag?
	tag = db.Column(db.String(30), nullable=False)

	user = db.relationship("User", backref=db.backref("tags",
													  order_by=tag_id))

	def __repr__(self):
		"""Displays useful info about tag when printed."""

		return "<Tag tag_id={}, tag={}, user={}, game={}>".format(self.tag_id,
																  self.tag,
														  		  self.user.username,
														  		  self.game.title)

class TagCategory(db.Model):  # Not implemented in HB version
	"""A category that a tag belongs to."""

	__tablename__ = "tag_cats"

	tag_cat_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	tag_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id'))
	# Which aspect of gaming is this tag for?
	# (i.e. 'genre', '# of players', 'gameplay')
	category = db.Column(db.String(30), nullable=False)
	color = db.Column(db.String(7), default='#D3D3D3')

	tag = db.relationship("Tag", backref=db.backref("tag_cats",
													order_by=tag_cat_id))

	def __repr__(self):
		"""Displays useful info about tag category when printed."""

		return "<Tag Category tag_cat_id={}, category={}>".format(self.tag_cat_id,
																  self.category)

class VgTag(db.Model):
	"""Association between games and tags."""

	__tablename__ = "vg_tags"

	vg_tag_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'))  # Which game are the tag(s) on?
	tag_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id'))  # Which tag(s) are on which game?

	game = db.relationship("Game", backref=db.backref("vg_tags",
													  order_by=vg_tag_id))
	tag = db.relationship("Tag", backref=db.backref("vg_tags",
													order_by=vg_tag_id))

	def __repr__(self):
		"""Displays useful info about video game tag when printed."""

		return "<VgTag vg_tag_id={}, game={}, tag={}>".format(self.vg_tag_id,
															 self.game.title,
															 self.tag.tag)


class Favorite(db.Model):  # Not implemented in HB version
	"""Games that have been bookmarked by the user."""

	__tablename__ = "faves"

	fave_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'))

	user = db.relationship("User", backref=db.backref("faves",
													  order_by=fave_id))

	game = db.relationship("Game", backref=db.backref("faves",
													  order_by=fave_id))

###################################################
# HELPER FUNCTIONS

def connect_to_db(app, db_uri='postgresql:///games'):
	"""Connect the database to Flask app."""

	# Configure to use PostgreSQL database
	app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.app = app
	db.init_app(app)

if __name__ == "__main__":

	from server import app
	connect_to_db(app)
	print "Connected to DB."  # Confirm on console that server is up.