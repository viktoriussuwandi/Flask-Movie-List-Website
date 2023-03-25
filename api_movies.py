import os, requests

class Movie_api :
  def __init__(self) :
    self.search_url  = os.environ['url_api']
    self.api_key     = os.environ['api_key']
    self.movie_list  = []

  def get_movie(self, title) :
    response    = requests.get(
      self.search_url, params = { 
        "api_key": self.api_key, "query": title 
      })
    self.movie_list = response.json()["results"]
    