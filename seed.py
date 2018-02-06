"""Utility file to seed games database from Kaggle data in seed_data/"""
from csv import reader

from model import (User, Game, Genre, VgGen, Difficulty, Comment,
				   Tag, TagCategory)

from model import connect_to_db, db 
from server import app

def parse_csv():
	"""Returns an iterable of game data."""

	# Read .csv file
	with open('seed_data/ign.csv') as csvfile:
		game_data = reader(csvfile, dialect='excel')

		# ID(0), descriptive score(1), title(2), ign URL(3), system(4),
		# critic score(5), genre(6), editors choice(7), year(8), month(9), day(10)
		return game_data

def load_games(game_data):
	"""Load games from ign.csv into database."""

	print "Games"

	Game.query.delete()  # Start with a fresh database
	
	for row in game_data:
		title = row[2]
		system = row[4]
		critic_score = row[5]

		game = Game(title=title,
					system=system,
					critic_score=critic_score)

		db.session.add(game)

	db.session.commit()

if __name__ == "__main__":
	connect_to_db(app)

	db.create_all()

	game_data = parse_csv()  # Only parse data once, then reuse below

	load_games(game_data)