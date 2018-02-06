"""Utility file to seed games database from Kaggle data in seed_data/"""
from csv import reader

from sqlalchemy import func
from model import (User, Game, Genre, VgGen, Difficulty, Comment,
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

		# ID(0), descriptive score(1), title(2), ign URL(3), system(4),
		# critic score(5), genre(6), editors choice(7), year(8), month(9), day(10)
		for row in game_data:
			title = row[2]
			system = row[4]
			critic_score = row[5]

			game = Game(title=title,
						system=system,
						critic_score=critic_score)

			db.session.add(game)

	db.session.commit()

def load_users():  # Do not use when done testing
	"""Load dummy data for users."""

	print "Fake users"

	User.query.delete()

	fake_user1 = User(username='ffluvr93',
					  email='ffluvr93@yahoo.com',
					  password='asecurepassword')

	fake_user2 = User(username='thecompletionist',
					  email='sirgamesalot@gmail.com',
					  password='password')

	fake_user3 = User(username='markiplier',
					  email='markiplier@gmail.com',
					  password='tinyboxtim')

	db.session.add_all([fake_user1, fake_user2, fake_user3])
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

if __name__ == "__main__":
	connect_to_db(app)

	db.create_all()

	load_games()
	load_users()
	set_val_game_id()