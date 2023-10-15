# llama_index.py

# Controls all of the LlamaIndex tools

import llama_index as llama_index
import requests
import wikipedia
import json

# Open and read the config.json file
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)


worldnews_api_key = config_data['WORLD_NEWS_API_KEY']
newsData_api_key = config_data['newsData_api_key']


#Wikipedia search
def wikipedia_search(country_name):
  try:
    country_info = wikipedia.page(country_name)
    country_wiki = country_info.content

  except wikipedia.exceptions.DisambiguationError as e:  
    return e.options


#news search
def get_country_news_worldnews(country_name):
    def search_news(worldnews_api_key, text, number=10, language='en', sort='publish-time', sort_direction='DESC'):
        url = "https://api.worldnewsapi.com/search-news"
        query = {
            'api-key': worldnews_api_key,
            'text': text,
            'number': str(number),
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
    country_news = search_news(worldnews_api_key, country_name, number=10)  # Adjust the number as needed

    # Format the news data and extract relevant information
    news_summaries = []
    if country_news:
        for news_item in country_news:
            headline = news_item.get('title', 'N/A')
            publication = news_item.get('source', 'N/A')
            date = news_item.get('published_datetime', 'N/A')
            summary = news_item.get('summary', 'N/A')

            # Create a dictionary for each news item
            news_summary = {
                'headline': headline,
                'publication': publication,
                'date': date,
                'summary': summary
            }

            news_summaries.append(news_summary)

    return news_summaries



## Alternate news API
import requests

def search_news(api_key, country_name, number=50, language='en', prioritydomain='top'):
    url = "https://newsdata.io/api/1/news"
    query = {
        'apikey': api_key,
        'qInTitle': country_name,
        'prioritydomain': prioritydomain,
        'language': language
    }
    response = requests.get(url, params=query)
    
    if response.status_code != 200:
        return {"error": f"Request failed with status code {response.status_code}"}

    return response.json()

def process_news_data(news_data):
    country_articles_list = []
    for news in news_data['results']:
        article = {
            'Headline': news['title'],
            'Source': news['creator'][0] if news['creator'] else 'Unknown',
            'Summary': news['description'],
            'Link': news['link'],
            'pubDate': news['pubDate'],
            'article_id': news['article_id'],
            'publication': news['source_id']
        }
        country_articles_list.append(article)
    
    return country_articles_list

# Main function to get country news
def get_country_news_newsdata(api_key, country_name):
    news_data = search_news(api_key, country_name)
    if "error" in news_data:
        return news_data["error"]
    
    country_articles_list = process_news_data(news_data)
    
    return country_articles_list

def write_news_summary(country_articles_list):
    news_summary = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "You are a highly skilled AI trained in language comprehension and summarization. Your task is to summarize the following news articles, focusing on their relevance to country risk, security, and stability. Retain only the most important points to offer a clear, coherent summary. Avoid unnecessary details. Include the headlines and links for the most significant stories."
            },
            {
                "role": "user",
                "content": country_articles_list
            }
        ]
    )
    return news_summary['choices'][0]['message']['content']

