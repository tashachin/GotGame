""" 'Got Game?' website."""

import babel.dates

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)

from flask_debugtoolbar import DebugToolbarExtension

from model import (User, Game, Genre, VgGen, Difficulty, Review, Tag,
                   TagCategory, VgTag)

from model import db, connect_to_db

from helper import *

app = Flask(__name__)

app.secret_key = "Placeholder"  # Look into .secret_key later

###################################################
# JINJA CONFIGS

app.jinja_env.undefined = StrictUndefined  # Provides better error message support

# https://stackoverflow.com/questions/4830535/python-how-do-i-format-a-date-in-jinja2

def format_datetime(value, format='medium'):  # Defaults to dd-MM-y
    """Allows conversion of datetimes in Jinja."""

    if format == 'full':
        format="EEEE, d. MMMM y"

    elif format == 'medium':
        format="dd-MM-y"

    return babel.dates.format_datetime(value, format)

app.jinja_env.filters['datetime'] = format_datetime  # You can customize Jinja filters!

###################################################
# APP ROUTES

@app.route('/')
def homepage():
    """Displays homepage."""

    return render_template('homepage.html')

@app.route('/search-results') 
def show_basic_results():  
    """A fun quick-search for the homepage."""

    title = request.args.get('title')

    games = retrieve_title(title)

    return render_template('search_results.html',
                           games=games)


@app.route('/login')
def show_login():
    """Show login page."""

    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    """Checks that user has entered correct password."""

    username = request.form.get('username')
    password = request.form.get('password')

    return check_credentials(username, password)


@app.route('/logout')
def logout():
    """Logs user out of site."""

    session.clear()
    flash("Logged out.")
    return redirect('/')


@app.route('/register')
def register():
    """Show new user registration form."""

    return render_template('register.html')


@app.route('/adv-search')
def advanced_search():
    """Displays advanced search options."""

    genres = Genre.query.all()
    
    return render_template('adv_search.html',
                           genres=genres)


@app.route('/adv-search-results')
def show_advanced_results():
    """Displays results after filters get applied."""

    critic_score = request.args.get('critic_score')
    aggregate_score = request.args.get('user_scores')
    platform = request.args.get('platform')
    specific_platform = request.args.get('specific_platform')
    genres = request.args.getlist('genre')

    vg_genres = VgGen.query.filter(VgGen.genre_id.in_(genres)).all()

    games = apply_filters(critic_score, aggregate_score, platform, specific_platform, genres)

    return render_template('search_results.html',
                           games=games,
                           vg_genres=vg_genres)


@app.route('/user/<user_id>')  # User profile page
def show_profile(user_id):

    user = retrieve_user(user_id)
    num_reviews, reviews = retrieve_user_reviews(user_id)

    return render_template('user_profile.html',
                           user=user,
                           num_reviews=num_reviews,
                           reviews=reviews)


@app.route('/edit-profile/<user_id>')
def edit_profile(user_id):

    user = retrieve_user(user_id)

    return render_template('edit_profile.html',
                           user=user)


@app.route('/update-bio', methods=['POST'])  # Will become defunct if using AJAX.
def update_user_bio():
    """Redirects user to their profile page once their bio has been added."""

    user_id = request.form.get('user_id')
    bio = request.form.get('user_bio')

    user = retrieve_user(user_id)
    user.bio = bio
    db.session.commit()

    return redirect('/user/' + user_id)


@app.route('/update-bio.json')
def json_user_bio():
    """Practicing AJAX calls."""
    
    
    pass

@app.route('/game/<platform>/<title>') # Game "profile" page
def show_game_profile(platform, title):
    
    game = Game.query.filter(Game.title == title, Game.platform == platform).one()
    game_id = game.game_id

    vg_genres = retrieve_genres(game_id)
    user_status = check_login_status()
    review = check_review_status(game)
    reviews = handle_review_status(game, user_status)
    tags = check_tags(user_status)

    return render_template('game_info.html',
                             game=game,
                             user_status=user_status,
                             review=review,
                             reviews=reviews,
                             vg_genres=vg_genres,
                             tags=tags)

@app.route('/new-user', methods=['POST'])
def validate_user():
    """Checks if username/email are already in use. 
    If not, register new user."""

    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    return process_registration(username, email, password)  # In helper.py

@app.route('/new-review.json', methods=['POST'])  # In a .json route, 'form data' needs to be passed as second arg
def get_review_info():
    """Return info about a game review as JSON."""

    # This will not work unless 'form data' gets passed through
    user_score = request.form.get('user_score')
    game_id = request.form.get('game_id')
    review = request.form.get('review')

    user_id = session['user_id']
    game = retrieve_game(game_id)

    create_review(game_id, review, user_score)
    update_aggregate_score(game)

    review_info = {
        "game_id": game_id,
        "user_score": user_score,
        "review": review,
    }

    print """<NEW REVIEW: game_id={}, user_score={}, review={}>""".format(game_id, 
                                                                          user_score, 
                                                                          review)
    return jsonify(review_info)


@app.route('/edit-review.json', methods=['POST'])
def edit_review():
    """Return info about user updating a game review as JSON."""

    user_score = request.form.get('edit_user_score')
    game_id = request.form.get('game_id')
    review_text = request.form.get('edit_review')

    user_id = session['user_id']
    game = retrieve_game(game_id)

    update_review(game_id, review_text, user_score)
    update_aggregate_score(game)

    review_data = {
        "game_id": game_id,
        "user_score": user_score,
        "review_text": review_text,
    }

    print "<UPDATED REVIEW: game_id={}, user_score={}, review={}>".format(game_id, 
                                                                          user_score, 
                                                                          review_text)
    return jsonify(review_data)


@app.route('/create-tags.json', methods=['POST'])
def get_tag_info():
    """Return info about a user's game tag as JSON."""

    tags = request.form.get('new_tags')
    tags = tags.split(',')

    user_id = session['user_id']

    tag_data = create_tags(user_id, tags)

    print "<CREATED NEW TAG: user_id={}, tags={}>".format(user_id, 
                                                          tags)

    return jsonify(tag_data)


@app.route('/update-tags.json', methods=['POST'])
def get_game_tag_info():
    """Attaches the user's selected tags to the current game they're viewing."""

    pass


###################################################
# DEBUGGING

if __name__ == "__main__":
    # Must be initialized as True when invoking DebugToolbarExtension
    app.debug = True
    # Prevents templates, etc. aren't cached during debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')