from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['form_token']
Bootstrap(app)

@app.route("/")
def home() :
  return render_template("index.html")


if __name__ == "__main__" :
  app.run(debug=True, host="0.0.0.0",port=2000)