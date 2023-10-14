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
def get_country_news_newsdata(country_name):
    def search_news(api_key, text, number=10, language='en', prioritydomain='top'): 
        url = "https://newsdata.io/api/1/news"
        query = {
            'apikey': api_key,
            'qInTitle': text,
            'prioritydomain': prioritydomain,
            'language': language
        }
        response = requests.get(url, params=query)
        
        if response.status_code != 200:
            return {"error": f"Request failed with status code {response.status_code}"}

        return response.json()

    api_key = newsData_api_key
    news_data = search_news(api_key, country_name, number=50)  # Adjust the number as needed
    country_articles_list = []
    
    for news in news_data['results']:
        title = news['title']
        content = news['content']
        summary = news['description']
        link = news['link']
        source = news['creator'][0] if news['creator'] else 'Unknown'
        publication = news['source_id']
        pubDate = news['pubDate']
        article_id = news['article_id']
        
        country_articles_list.append({
            'Headline': title,
            'Source': source,
            'Summary': summary,
            'Link': link,
            'pubDate': pubDate,
            'article_id': article_id,
            'publication': publication
        })    

    for news in country_articles_list:
        print(f"Headline: {news['Headline']}")
        print(f"Source: {news['Source']}")
        print(f"Summary: {news['Summary']}")
        print(f"Link: {news['Link']}")
        print(f"Date: {news['pubDate']}")
        print("\n")

    news_articles_str = "\n".join([f"Headline: {article['Headline']}\nSource: {article['Source']}\nSummary: {article['Summary']}\nLink: {article['Link']}\nDate: {article['pubDate']}\n" for article in country_articles_list])

    return news_articles_str
    print(news_articles_str)
