from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

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
  id          = db.Column(db.Integer, primary_key = True)
  title       = db.Column(db.String(250), unique=True, nullable=False)
  year        = db.Column(db.Integer, nullable=False)
  description = db.Column(db.String, nullable=False)
  rating      = db.Column(db.Float, nullable=False)
  ranking     = db.Column(db.Float, nullable=False)
  review      = db.Column(db.String(250), nullable=False)
  img_url     = db.Column(db.String, nullable=False)

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


# ---------------------------------------------------------------------------------------
# WTF FORM VALIDATION FUNCTION
# ---------------------------------------------------------------------------------------

    
# ---------------------------------------------------------------------------------------
# ROUTING FUNCTIONS
# ---------------------------------------------------------------------------------------

@app.route("/")
def home() :
  first_movies()
  all_movies  = Movies.query.all()
  return render_template("index.html", movies = all_movies)

# ---------------------------------------------------------------------------------------
# HOST-PORT
# ---------------------------------------------------------------------------------------
if __name__ == "__main__" :
  app.run(debug=True, host="0.0.0.0",port=2000)