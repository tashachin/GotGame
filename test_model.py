"""Modularizes example data."""

from model import *

def example_data():
	"""Adds all example data to a database"""

	for obj in create_users():
		db.session.add(obj)

	for obj in create_games():
		db.session.add(obj)

	for obj in create_genres():
		db.session.add(obj)

	for obj in create_vg_genres():
		db.session.add(obj)

	for obj in create_difficulties():
		db.session.add(obj)

	db.session.add(create_reviews())

	for obj in create_tags():
		db.session.add(obj)

	for obj in create_tag_cats():
		db.session.add(obj)

	for obj in create_vg_tags():
		db.session.add(obj)

	db.session.commit()

def create_users(): # Will be user-populated
	"""Returns user objects to be added."""
	user1 = User(username='ffluvr93',
				 email='ffluvr93@yahoo.com',
				 password='asecurepassword')

	user2 = User(username='thecompletionist',
				 email='sirgamesalot@gmail.com',
				 password='password')

	user3 = User(username='markiplier',
				 email='markiplier@gmail.com',
				 password='tinyboxtim')

	return user1, user2, user3

def create_games():  # Will be seeded AND user-populated
	"""Returns game objects to be added."""
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

	return game1, game2, game3

def create_genres():  # Will be seeded(?) NOT user-populated
	"""Returns genre objects to be added."""  
	# Can test features needing genre data without worrying about parsing csv yet

	genre1 = Genre(genre_type='Platformer')

	genre2 = Genre(genre_type='Action')

	genre3 = Genre(genre_type='Adventure')

	genre4 = Genre(genre_type='Visual Novel')

	genre5 = Genre(genre_type='Puzzle')

	genre6 = Genre(genre_type='Horror')

	return genre1, genre2, genre3, genre4, genre5, genre6

def create_vg_genres():  # NOT user-populated
	"""Returns vg-genre association objects to be added."""

	vg_genre1 = VgGen(game_id=2,
					  genre_id=1)

	vg_genre2 = VgGen(game_id=1,
					  genre_id=5)

	return vg_genre1, vg_genre2

def create_difficulties():  # ???? ask advisor how this table links to everything
	"""Returns difficulty objects to be added."""

	diff1 = Difficulty(game_id=3,
					   level=9)
	diff2 = Difficulty(game_id=1,
					   level=4)

	return diff1, diff2

def create_reviews():  # Will be user-populated
	"""Returns review objects to be added."""

	review = Review(user_id=1,
					  game_id=1,
					  review='Literally the best game ever.')

	return review

def create_tags():  # Will be user-populated
	"""Returns tag objects to be added."""

	tag1 = Tag(user_id=1,
			  game_id=1,
			  tag='Recommend')

	tag2 = Tag(user_id=1,
			   game_id=1,
			   tag='High Fant')

	return tag1, tag2

def create_tag_cats():  # NOT user-generated
	"""Returns tag category objects to be added."""

	tag_cat1 = TagCategory(tag_id=1,
						   category='custom')

	tag_cat2 = TagCategory(tag_id=1,
						   category='genre')

	return tag_cat1, tag_cat2

def create_vg_tags():  # Will be user-populated
	"""Returns vg-tag association objects to be added."""

	vg_tag1 = VgTag(game_id=1,
					tag_id=1)

	vg_tag2 = VgTag(game_id=1,
					tag_id=2)

	return vg_tag1, vg_tag2
