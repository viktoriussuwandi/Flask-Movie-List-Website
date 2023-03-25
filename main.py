from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

from api_movies import Movie_api
from forms import UpdateForm, AddForm
import os

# ---------------------------------------------------------------------------------------
# ADDITIONAL DATABASE FUNCTIONS
# ---------------------------------------------------------------------------------------
def add_movie(movie) :
  try :
    db.session.add(movie)
    return db.session.commit()
  except exc.IntegrityError :
    # print('Duplicate data')
    db.session.rollback()
    return False

def first_movies(first_use = False) :
  count_data    = Movies.query.count()
  if count_data == 0 and first_use == True :
    init_movie    = Movies(
      id          = 1,
      title       = "Phone Booth",
      year        = 2002,
      description = "Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
      rating      = 7.3,
      ranking     = 10,
      review      = "My favourite character was the caller.",
      img_url     = "https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
    )
    add_movie(init_movie)
    
# ---------------------------------------------------------------------------------------
# FLASK APP, API, & DATABASE
# ---------------------------------------------------------------------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['form_token']
Bootstrap(app)
API   = Movie_api()

app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book-collection.db'
app.config ['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

class Movies(db.Model) :
  id          = db.Column("id",db.Integer, primary_key = True)
  title       = db.Column("title",db.String(250), unique=True, nullable=False)
  year        = db.Column("year",db.Integer, nullable=False)
  description = db.Column("description",db.String, nullable=False)
  rating      = db.Column("rating",db.Float, nullable=False)
  ranking     = db.Column("ranking",db.Float, nullable=False)
  review      = db.Column("review",db.String(250), nullable=False)
  img_url     = db.Column("img_url",db.String, nullable=False)

  def __repr__(self) :
    return '<Movies {self.title}>'

with app.app_context() : 
  db.create_all()
  first_movies(first_use = True)

# ---------------------------------------------------------------------------------------
# ROUTING FUNCTIONS
# ---------------------------------------------------------------------------------------
@app.route("/")
def home() :
  all_movies  = Movies.query.all()
  return render_template("index.html", movies = all_movies)

@app.route("/update", methods = ["GET", "POST"])
def update() :
  movie_id    = request.args.get('id')
  find_movie  = Movies.query.get(movie_id)
  update_form = UpdateForm()
  
  if request.method == "GET" :
    update_form.rating.data = find_movie.rating
    update_form.review.data = find_movie.review 
  elif update_form.validate_on_submit() :
    find_movie.rating = update_form.rating.data
    find_movie.review = update_form.review.data
    db.session.commit()
    return redirect("/")
  
  movie_data  = {}
  movie_data["movie"] = find_movie
  movie_data["form"]  = update_form
  return render_template("update.html", data = movie_data)

@app.route("/delete")
def delete() :
  movie_id    = request.args.get('id')
  find_movie  = Movies.query.get(movie_id)
  db.session.delete(find_movie)
  db.session.commit()
  return redirect('/')

@app.route("/add", methods = ["GET", "POST"])
def add() :
  add_form = AddForm()
  if request.method == "POST" and add_form.validate_on_submit() :
    movie_title = add_form.title.data
    API.get_movie(movie_title)
    movie_list = API.movie_list
    return render_template("select.html", movies = movie_list)
  return render_template("add.html", form = add_form)

@app.route("/select", methods =["GET", "POST"])
def select() :
  api_id = request.args.get('id')
  movie_list = API.movie_list
  data = {"api_id" : api_id, "movies" : movie_list}
  return data

  
# ---------------------------------------------------------------------------------------
# HOST-PORT
# ---------------------------------------------------------------------------------------
if __name__ == "__main__" :
  app.run(debug=True, host="0.0.0.0",port=2000)

