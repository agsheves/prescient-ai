# Controls all of the LlamaIndex tools

import llama_index as llama_index
import requests
import wikipedia
import json

# Open and read the config.json file
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)


worldnews_api_key = config_data['WORLD_NEWS_API_KEY']


#Wikipedia search
def wikipedia_search(country_name):
  try:
    country_info = wikipedia.page(country_name)
    country_wiki = country_info.content

  except wikipedia.exceptions.DisambiguationError as e:  
    return e.options





#news search

def get_country_news(country_name):
  def search_news(worldnews_api_key, text, number=10, language='en', sort='publish-time', sort_direction='DESC'):
      url = "https://api.worldnewsapi.com/search-news"
      query = {
          'api-key': worldnews_api_key,
          'text': text,
          'number': number,
          'language': language,
          'sort': sort,
          'sort-direction': sort_direction
      }
      response = requests.get(url, params=query)

      # Check if request was successful
      if response.status_code == 200:
          return response.json()
      else:
          print(f"Request failed with status code {response.status_code}")
          return None


  # Call the API without the date constraint
  country_news = search_news(worldnews_api_key, country_name, number=50)
