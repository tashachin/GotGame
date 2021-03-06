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

    elif format == 'birthday':
        format='MM-dd'

    return babel.dates.format_datetime(value, format)

app.jinja_env.filters['datetime'] = format_datetime  # You can customize Jinja filters!

###################################################
# APP ROUTES

@app.route('/')
def homepage():
    """Displays homepage."""

    return render_template('homepage.html')

@app.route('/search-results') 
def show_results():  
    """Queries the database and returns all games that satisfy the user's 
    search filters."""

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
    tags = check_tags(user_id)

    return render_template('user_profile.html',
                           user=user,
                           num_reviews=num_reviews,
                           reviews=reviews,
                           tags=tags)


@app.route('/edit-profile/<user_id>')
def edit_profile(user_id):

    user = retrieve_user(user_id)

    return render_template('edit_profile.html',
                           user=user)


@app.route('/update-profile', methods=['POST'])  # FIX ME: What if user wants to delete info?
def update_user_bio():
    """Redirects user to their profile page once their bio has been added."""

    user_id = request.form.get('user_id')
    bio = request.form.get('user_bio')
    location = request.form.get('user_location')
    birthday = request.form.get('user_birthday')

    user = retrieve_user(user_id)

    if bio:
        user.bio = bio

    if location:
        user.location = location

    if birthday:
        datetime_obj = datetime.strptime(birthday, '%m-%d-%Y')
        formatted_birthday = datetime_obj.strftime('%Y-%m-%d')
        user.birthday = formatted_birthday

    db.session.commit()

    flash('Your changes have been saved.')
    return redirect('/user/' + user_id)


@app.route('/game/<platform>/<path:title>') # Game "profile" page
def show_game_profile(platform, title):
    
    game = Game.query.filter(Game.title == title, Game.platform == platform).one()
    game_id = game.game_id

    vg_genres = retrieve_genres(game_id)
    user_status = check_login_status()
    review = check_review_status(game)
    reviews = handle_review_status(game, user_status)
    tags = check_tags(user_status)
    vg_tags = check_vg_tags(game_id)
    all_tagged_games = retrieve_all_tagged_games(vg_tags)

    return render_template('game_info.html',
                             game=game,
                             user_status=user_status,
                             review=review,
                             reviews=reviews,
                             vg_genres=vg_genres,
                             tags=tags,
                             vg_tags=vg_tags,
                             all_tagged_games=all_tagged_games)

@app.route('/new-user', methods=['POST'])
def validate_user():
    """Checks if username/email are already in use. 
    If not, register new user."""

    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    return process_registration(username, email, password)  # In helper.py

@app.route('/review.json', methods=['POST'])  # In a .json route, 'form data' needs to be passed as second arg
def get_review_info():
    """Return info about a game review as JSON."""

    # This will not work unless 'form data' gets passed through
    user_score = request.form.get('user_score')
    game_id = request.form.get('game_id')
    review = request.form.get('review')

    user_id = session['user_id']
    game = retrieve_game(game_id)

    review_status = check_review_status(game)

    if review_status:
        update_review(game_id, review, user_score)
    
    else:
        create_review(game_id, review, user_score)
    
    update_aggregate_score(game)

    review_info = {
        "game_id": game_id,
        "user_score": user_score,
        "review": review,
    }

    print """<REVIEW: game_id={}, user_score={}, review={}>""".format(game_id, 
                                                                      user_score, 
                                                                      review)
    return jsonify(review_info)


@app.route('/create-tags.json', methods=['POST'])
def get_tag_info():
    """Return info about a user's game tag as JSON."""

    tags = request.form['data']
    tags = tags.split(',')

    user_id = session['user_id']

    tag_data = create_tags(user_id, tags)

    print "<CREATED NEW TAG: user_id={}, tags={}>".format(user_id, 
                                                          tags)

    return jsonify(tag_data)


@app.route('/delete-tags.json', methods=['POST'])
def remove_user_tags():
    """Allows user to delete tags they've created."""

    tag_ids = request.form.getlist('data[]')

    delete_tags(tag_ids)

    return jsonify({})


@app.route('/update-tags.json', methods=['POST'])
def get_game_tag_info():
    """Attaches the user's selected tags to the current game they're viewing."""

    game_id = request.form.get('game')
    tag_ids = request.form.getlist('data[]')

    vg_tag_data = create_vg_tags(game_id, tag_ids)
    
    return jsonify(vg_tag_data)


@app.route('/delete-game-tags.json', methods=['POST'])
def remove_game_tag_info():
    """Deletes whichever tags the user removes from the current game."""

    game_id = request.form.get('game')
    vg_tag_ids = request.form.getlist('data[]')

    vg_tag_data = remove_vg_tags(game_id, vg_tag_ids)

    return jsonify({})


@app.route('/tag/<tag>/<user_id>')
def show_tagged_games(tag, user_id):
    """Displays all the games a user has tagged with a specific tag."""

    games = retrieve_vg_tags(tag, user_id)

    return render_template('tagged_games.html',
                           games=games)

###################################################
# DEBUGGING

if __name__ == "__main__":
    # Must be initialized as True when invoking DebugToolbarExtension
    # app.debug = True
    # # Prevents templates, etc. aren't cached during debug mode
    # app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')