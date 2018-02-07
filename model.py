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
	platform = db.Column(db.String(25), nullable=True)  # What console version is this game?
	critic_score = db.Column(db.Float, nullable=False)
	user_score = db.Column(db.Float, nullable=True)

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

	def __repr__(self):
		"""Displays useful info about comment when printed."""

		return "<Comment comment_id={}, user={}, game={}>".format(self.comment_id,
																  self.user.username,
																  self.game.title)

class Tag(db.Model):
	"""A user-generated tag to label a game."""

	__tablename__ = "tags"

	tag_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id')) # Who created the tag?
	game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'))  # Which game is the tag associated with?
	tag = db.Column(db.String(30), nullable=False)

	user = db.relationship("User", backref=db.backref("tags",
													  order_by=tag_id))
	game = db.relationship("Game", backref=db.backref("tags",
													  order_by=tag_id))

	def __repr__(self):
		"""Displays useful info about tag when printed."""

		return "<Tag tag_id={}, tag={}, user={}, game={}>".format(self.tag_id,
																  self.tag,
														  		  self.user.username,
														  		  self.game.title)

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

		return "<VgTag vg_tag_id={}, game={}, tag={}".format(self.vg_tag_id,
															 self.game.title,
															 self.tag.tag)

###################################################
# HELPER FUNCTIONS

def connect_to_db(app, db_uri='postgresql:///games'):
	"""Connect the database to Flask app."""

	# Configure to use PostgreSQL database
	app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.app = app
	db.init_app(app)

def example_data():
	"""Create example data for test database."""

	##### USERS #####
	user1 = User(username='ffluvr93',
				 email='ffluvr93@yahoo.com',
				 password='asecurepassword')

	user2 = User(username='thecompletionist',
				 email='sirgamesalot@gmail.com',
				 password='password')

	user3 = User(username='markiplier',
				 email='markiplier@gmail.com',
				 password='tinyboxtim')

	##### GAMES #####
	game1 = Game(title='Best Game Ever',
				 platform='Xbox 360',
				 critic_score=9.5,
				 user_score=9.8)

	game2 = Game(title='So-So Game',
				 platform='Nintendo 64',
				 critic_score=6.5,
				 user_score=7.2)

	game3 = Game(title='Bargain Bin Game',
				 platform='Playstation 2',
				 critic_score=3.0,
				 user_score=2.0)

	##### GENRES #####

	genre1 = Genre(genre_type='Platformer')

	genre2 = Genre(genre_type='Action')

	genre3 = Genre(genre_type='Adventure')

	genre4 = Genre(genre_type='Visual Novel')

	genre5 = Genre(genre_type='Puzzle')

	genre6 = Genre(genre_type='Horror')

	##### VIDEO GAME - GENRES #####

	vg_genre1 = VgGen(game_id=2,
					  genre_id=1)

	vg_genre2 = VgGen(game_id=1,
					  genre_id=5)

	##### DIFFICULTY ##### user-generated

	diff1 = Difficulty(game_id=3,
					   level=9)
	diff2 = Difficulty(game_id=1,
					   level=4)

	##### COMMENTS ##### user-generated

	comment = Comment(user_id=1,
					  game_id=1,
					  comment='Literally the best game ever.')

	##### TAGS ##### user-generated

	tag1 = Tag(user_id=1,
			  game_id=1,
			  tag='Recommend')

	tag2 = Tag(user_id=1,
			   game_id=1,
			   tag='High Fant')

	##### TAG CATEGORIES #####

	tag_cat1 = TagCategory(tag_id=1,
						   category='custom')

	tag_cat2 = TagCategory(tag_id=1,
						   category='genre')

	##### VG TAGS #####

	vg_tag1 = VgTag(game_id=1,
					tag_id=1)

	vg_tag2 = VgTag(game_id=1,
					tag_id=2)

	db.session.add_all([user1, user2, user3,
						game1, game2, game3,
						genre1, genre2, genre3, genre4, genre5, genre6,
						vg_genre1, vg_genre2,
						diff1, diff2,
						comment,
						tag1, tag2,
						tag_cat1, tag_cat2,
						vg_tag1, vg_tag2])

	db.session.commit()

if __name__ == "__main__":

	from server import app
	connect_to_db(app)
	print "Connected to DB."  # Confirm on console that server is up.