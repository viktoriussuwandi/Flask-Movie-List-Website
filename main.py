from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, DecimalField
from wtforms.validators import DataRequired, NumberRange, length

# ---------------------------------------------------------------------------------------
# FLASK APP & DATABASE
# ---------------------------------------------------------------------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['form_token']
Bootstrap(app)

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
    
with app.app_context() : db.create_all()

# ---------------------------------------------------------------------------------------
# DATABASE FUNCTIONS
# ---------------------------------------------------------------------------------------
def add_movie(movie) :
  try :
    db.session.add(movie)
    return db.session.commit()
  except exc.IntegrityError :
    # print('Duplicate data')
    db.session.rollback()
    return False

def first_movies() :
  count_data    = Movies.query.count()
  if count_data == 0 :
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
# WTF FORM VALIDATION FUNCTION
# ---------------------------------------------------------------------------------------
class UpdateForm(FlaskForm) :
  rating      = DecimalField(  label = "Rating", 
                               validators = [ NumberRange(min=0,max=10) ] )
  description = TextAreaField( label  = "Description", 
                               validators = [ DataRequired(), length(max=250) ] )
  submit      = SubmitField(   label  = "Submit")

# ---------------------------------------------------------------------------------------
# ROUTING FUNCTIONS
# ---------------------------------------------------------------------------------------
@app.route("/")
def home() :
  first_movies()
  all_movies  = Movies.query.all()
  return render_template("index.html", movies = all_movies)

@app.route("/update", methods = ["GET", "POST"])
def update() :
  movie_id    = request.args.get('id')
  find_movie  = Movies.query.get(movie_id)
  update_form = UpdateForm()
  
  if request.method == "GET" :
    update_form.rating.data      = find_movie.rating
    update_form.description.data = find_movie.description 
  else :
    find_movie.rating      = update_form.rating.data
    find_movie.description = update_form.description.data
    db.session.commit()
    return redirect("/")
  
  movie_data  = {}
  movie_data["movie"] = find_movie
  movie_data["form"]  = update_form
  return render_template("update.html", data = movie_data)

@app.route("/select")
def delete() :
  return render_template("select.html")
  
@app.route("/add")
def add() :
  return render_template("add.html")

# ---------------------------------------------------------------------------------------
# HOST-PORT
# ---------------------------------------------------------------------------------------
if __name__ == "__main__" :
  app.run(debug=True, host="0.0.0.0",port=2000)


# Example API request :
# https://api.themoviedb.org/3/movie/550?api_key=43f74160b22cece803a5937d1909912f
  
# API Key (v3 auth) :
# 43f74160b22cece803a5937d1909912f

# API Read Access Token (v4 auth):
# eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0M2Y3NDE2MGIyMmNlY2U4MDNhNTkzN2QxOTA5OTEyZiIsInN1YiI6IjVlOTFjNTg2YmVmYjA5MDAxYWJkMzQ3NSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.EcBJQhnxurpW-O7SjuIWOg1VstVFwNqdT0s4eeEtsLo

