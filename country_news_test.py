# Test country news.

import requests
import json
from llama_index import get_country_news_worldnews  # Import the function you want to test
from llama_index import get_country_news_newsdata

# Open and read the config.json file
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)

worldnews_api_key = config_data['WORLD_NEWS_API_KEY']


# Call the function with a country name
country_name = "Iran"  # Replace with the country you want to test
news_summaries = get_country_news_newsdata(country_name)
print(news_summaries)

# Display the results
for index, news_summary in enumerate(news_summaries, start=1):
    print(f"News Article {index}:")
    print(f"Headline: {news_summary['Headline']}")
    print(f"Source: {news_summary['Source']}")
    print(f"Date: {news_summary['pubDate']}")
    print(f"Summary: {news_summary['Summary']}\n")




