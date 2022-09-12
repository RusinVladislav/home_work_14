from flask import Flask, render_template
from utils import get_movie_by_title, get_movie_by_years, get_movie_by_rating, get_movie_by_genre, \
    get_movie_by_two_actors, get_movie_by_type_year_genre, get_list_actors_more_2

app = Flask(__name__)


# ШАГ 0
# для удобства проверки домашнего задания создал вьюшку с сылками на соответствующие шаги в домашке
@app.route("/")
def page_main():
    return render_template('main.html')


# ШАГ 1
@app.route("/movie/<title>")
def page_movie(title):
    movie = get_movie_by_title(title)
    return render_template('list_movie.html', movie=movie)


# ШАГ 2
@app.route("/movie/<int:year_1>/to/<int:year_2>")
def page_movie_by_years(year_1, year_2):
    movie = get_movie_by_years(year_1, year_2)
    return render_template('list_movie.html', movie=movie)


# ШАГ 3
@app.route("/rating/<rating>")
def page_movie_by_rating(rating):
    movie = get_movie_by_rating(rating)
    return render_template('list_movie.html', movie=movie)


# ШАГ 4
@app.route("/genre/<genre>")
def page_movie_by_genre(genre):
    movie = get_movie_by_genre(genre)
    return render_template('list_movie.html', movie=movie)


# ШАГ 5
# решил все же набросать вьюшку - с ней как-то приятней да и видна работа
@app.route("/twoactors/<names>")
def page_movie_by_two_actors(names):
    movie = get_movie_by_two_actors(names)
    actors = get_list_actors_more_2(names)
    return render_template('list_movie.html', movie=movie, actors=actors)


# ШАГ 6
# решил все же набросать вьюшку - с ней как-то приятней да и видна работа
@app.route("/customserch/<tupe>/<int:year>/<genre>")
def page_movie_by_type_year_genre(tupe, year, genre):
    movie = get_movie_by_type_year_genre(tupe, year, genre)
    return render_template('list_movie.html', movie=movie)


if __name__ == '__main__':
    app.run(debug=True)
