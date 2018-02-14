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
	load_genres()
	load_game_genres()
	set_val_game_id()