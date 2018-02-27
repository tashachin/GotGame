"""Utility file to seed games database from Kaggle data in seed_data/"""
from csv import reader

from sqlalchemy import func
from model import (User, Game, Genre, VgGen, Difficulty, Review,
				   Tag, TagCategory)

from model import connect_to_db, db 
from server import app

def load_games():
	"""Load games from ign.csv into database."""

	print "Games"

	Game.query.delete()  # Start with a fresh database
	
	with open('seed_data/ign.csv') as csvfile:
		game_data = reader(csvfile, dialect='excel')

		next(game_data)  # Skips header row

		# ID(0), descriptive score(1), title(2), ign URL(3), platform(4),
		# critic score(5), genre(6), editors choice(7), year(8), month(9), day(10)
		for row in game_data:
			title = row[2]
			platform = row[4]
			critic_score = row[5]

			game = Game(title=title,
						platform=platform,
						critic_score=critic_score)

			db.session.add(game)

	db.session.commit()


def load_genres():
	"""Load genres into a separate table."""

	print "Genres"

	Genre.query.delete()

	with open('seed_data/ign.csv') as csvfile:
		game_data = reader(csvfile, dialect='excel')

		next(game_data)

		for row in game_data:
			genres = row[6]
			genre_types = genres.split(',')
				
			for genre_type in genre_types:

				if Genre.query.filter(Genre.genre_type == genre_type).first() or "":
					pass
					
				else:
					genre = Genre(genre_type=genre_type)

					db.session.add(genre)
					db.session.commit()


def load_game_genres():
	"""Link genres of games into a middle table."""

	print "Game Genres"

	VgGen.query.delete()

	with open('seed_data/ign.csv') as csvfile:
		game_data = reader(csvfile, dialect='excel')

		next(game_data)

		for row in game_data:
			title = row[2]
			platform = row[4]
			genres = row[6]
			genre_types = genres.split(',')

			game = Game.query.filter(Game.title == title, Game.platform == platform).first()
			game_id = game.game_id

			for genre_type in genre_types:

				genre = Genre.query.filter(Genre.genre_type == genre_type).one()
				genre_id = genre.genre_id

				vg_genre = VgGen(game_id=game_id,
								 genre_id=genre_id)

				db.session.add(vg_genre)
				db.session.commit()

###########################
# FOR TESTING

def load_test_user():
	"""Load user for testing."""

	print "Test User"

	user = User(username='markiplier',
				email='markiplier@mark.com',
				password='markiplier',
				birthday='1989-06-28',
				location='LA',
				bio='Hello, everybody! My name is Markiplier.',
				fave_game="Sid Meier's Civilization V")

	db.session.add(user)
	db.session.commit()

	print "Reviews"

	review1 = Review(user_id=1,
					 game_id=16053,
					 user_score=8,
					 review="""
					 An action-packed romp through a zombie-infested island.
					 Needs more dakka.""")
	review2 = Review(user_id=1,
					 game_id=17979,
					 user_score=9,
					 review="""
					 A disgustingly sad game. A solid platformer, though.
					 Has a lot of replayability value.
					 Looking forward to future add-ons.""")
	review3 = Review(user_id=1,
					 game_id=16360,
					 user_score=10,
					 review="""
					 I'm rendered speechless.
					 A beautiful game. Please play this game.""")
	review4 = Review(user_id=1,
					 game_id=17484,
					 user_score=9,
					 review="""
					 They should probably make this multiplayer.
					 Just a thought.
					 That being said, the single-player campaign is fantastic.""")

	db.session.add_all(review1, 
					   review2, 
					   review3, 
					   review4, 
					   review5)
	db.session.commit()

	print "Tags"

	tag1 = Tag(user_id=1,
			   tag='horror')
	tag2 = Tag(user_id=1,
               tag='rec')
	tag3 = Tag(user_id=1,
               tag='zombies')
	tag4 = Tag(user_id=1,
               tag='fave')
	tag5 = Tag(user_id=1,
               tag='streamed')

	db.session.add_all(tag1, 
					   tag2, 
					   tag3, 
					   tag4, 
					   tag5)
	db.session.commit()

	print "Vg Tags"

	vg_tag1 = VgTag(game_id=16053,
                    tag_id=1)
	vg_tag2 = VgTag(game_id=16053,
                    tag_id=3)
	vg_tag3 = VgTag(game_id=16360,
                    tag_id=2)
	vg_tag4 = VgTag(game_id=17484,
                    tag_id=1)
	vg_tag5 = VgTag(game_id=17484,
                    tag_id=2)
	vg_tag6 = VgTag(game_id=17484,
                    tag_id=4)
	vg_tag7 = VgTag(game_id=16053,
                    tag_id=5)
	vg_tag8 = VgTag(game_id=17979,
                    tag_id=2)
	vg_tag9 = VgTag(game_id=8838,
                    tag_id=2)
	vg_tag10 = VgTag(game_id=1,
                    tag_id=4)

	db.session.add_all(vg_tag1, 
					   vg_tag2, 
					   vg_tag3, 
					   vg_tag4, 
					   vg_tag5,
					   vg_tag6,
					   vg_tag7,
					   vg_tag8,
					   vg_tag9,
					   vg_tag10)
	db.session.commit()

def set_val_game_id():
	"""Set value for the next game_id after seeding database."""

	# Retrieve most recent game_id added to database
	result = db.session.query(func.max(Game.game_id)).one()
	max_id = int(result[0])

	# Set value of the new game_id to be max_id + 1
	query = "SELECT setval('games_game_id_seq', :new_id)"
	db.session.execute(query, {'new_id': max_id + 1})
	db.session.commit()


def set_val_user_id():
	"""Set value for the next user_id after seeding database."""

	result = db.session.query(func.max(User.user_id)).one()
	max_id = int(result[0])

	query = "SELECT setval('users_user_id_seq', :new_id)"
	db.session.execute(query, {'new_id': max_id + 1})
	db.session.commit()


def set_val_review_id():
	"""Set value for the next review_id after seeding database."""

	result = db.session.query(func.max(Review.review_id)).one()
	max_id = int(result[0])

	query = "SELECT setval('reviews_review_id_seq', :new_id)"
	db.session.execute(query, {'new_id': max_id + 1})
	db.session.commit()


def set_val_tag_id():
	"""Set value for the next tag_id after seeding database."""

	result = db.session.query(func.max(Tag.tag_id)).one()
	max_id = int(result[0])

	query = "SELECT setval('tags_tag_id_seq', :new_id)"
	db.session.execute(query, {'new_id': max_id + 1})
	db.session.commit()


def set_val_vg_tag_id():
	"""Set value for the next vg_tag_id after seeding database."""

	result = db.session.query(func.max(VgTag.vg_tag_id)).one()
	max_id = int(result[0])

	query = "SELECT setval('vg_tags_vg_tag_id_seq', :new_id)"
	db.session.execute(query, {'new_id': max_id + 1})
	db.session.commit()


if __name__ == "__main__":
	connect_to_db(app)

	db.create_all()

	load_games()
	load_genres()
	load_game_genres()
	load_test_user()
	set_val_game_id()
	set_val_user_id()
	set_val_review_id()
	set_val_tag_id()
	set_val_vg_tag_id()
