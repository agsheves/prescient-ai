# ai_toolkit.py

import numpy as np
import os
import openai
from colorama import init, Fore, Style
from llama_index import wikipedia_search
from llama_index import get_country_news_worldnews
from llama_index import get_country_news_newsdata
from llama_index import write_news_summary
import json

with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)

openai.api_key = config_data['OPENAI_API_KEY']

ai_tools = ['country risk analyst', 'auditor', 'general researcher']



## Task routing assesses the user input and chooses the appropriate tool for the job

def task_routing(user_input):
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": f"""You are a world-
      class project manager and excel at choosing the right tool or team for the job. 
      Review the user request and select the most approperiate tool from these options {ai_tools}" You must return one of these tools or, if you are unsure, ask for additiona' clarification."""},
      {"role": "user", "content": user_input}
    ],
    stream=False
  )
  
  assistant_msg = response.choices[0].message['content']
  
  # Selects the specialized tool for the task or defaults to default main model
  if 'country risk analyst' in assistant_msg:
    print(Fore.WHITE + "Staring the country risk tool...")
    country_name = input(Fore.WHITE + "Please confirm the country name: ")
    country_wiki = wikipedia_search(country_name)
    country_news = get_country_news_newsdata(country_name)
    summarized_news = write_news_summary(country_news)

    
    # Modify the conversation history to include country_news
    country_conversation_history = [
        {"role": "system", "content": "You are an expert geopolitical and security analyst. You produce succinct, insightful country risk assessments looking at both the obvious more subtle factors. Keep your answers short and offer to provide more detail if necessary. Prompt the user for additional context where necessary."},
        {"role": "user", "content": user_input}
    ]
    
    country_risk_chat(user_input, summarized_news, country_news, country_wiki)

  elif 'auditor' in assistant_msg:
    print(Fore.WHITE + "--Starting the auditor tool--")
  elif 'general researcher' in assistant_msg:
    print(Fore.WHITE + "--Starting the default chat model--")
    default_chat(user_input)
  else:
    print(Fore.WHITE + "--Starting the default chat model--")
    default_chat(user_input)

    pass
  

## DEFAULT
## Uses a standard chat interface for non-techncial questions

default_conversation_history = [
  {"role": "system", "content": "You are a helpful assistant. You provide clear, succinct answers with the minimum of unnecessary explanation or background. Keep your answers short and offer to provide more detail if necessary"}
]

def default_chat(user_input):
  global default_conversation_history  # Access the global conversation history
  default_conversation_history.append({"role": "user", "content": user_input})  
  # Append the user's message to the conversation history

  response = openai.ChatCompletion.create(
      model="gpt-4",
      messages=default_conversation_history,  
    # Use the conversation history in the API call
      stream=False
  )

  assistant_msg = response.choices[0].message['content']
  default_conversation_history.append({"role": "assistant", "content": assistant_msg})  # Append the assistant's message to the conversation history

  print(Fore.WHITE + assistant_msg)
  print("\n")
  user_input = input(Fore.BLUE + "-->")
  default_chat(user_input)



## Country Risk
## Uses a tailored prompt for country risk discussions

country_conversation_history = [
  {"role": "system", "content": "You are an expert geopolitical and security analyst. You produce succinct, insightful country risk assessments looking at both the obvious more subtle factors. Keep your answers short and offer to provide more detail if necessary. Prompt the user for addituional context where necessary."}
]

# Modify the country_risk_chat function
def country_risk_chat(user_input, summarized_news, full_news, country_wiki):
    # Show summarized news first
    print(Fore.WHITE + f"Here's a summary of the latest news:\n{summarized_news}")

    # Prepare assistant's message for risk assessment
    assistant_response = [
        {"role": "system", "content": f"You are an expert in geopolitical and security analysis. For this risk assessment, consider the following summarized news and Wikipedia information:\n{summarized_news}\n{country_wiki[:200]}..."},
        {"role": "user", "content": user_input}
    ]

    # Use the assistant_response in the Chat API call
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=assistant_response,
        stream=False
    )
    
    assistant_msg = response.choices[0].message['content']
    print(Fore.WHITE + assistant_msg)
    print("\n")
    next_user_input = input(Fore.BLUE + "-->")
    country_risk_chat(next_user_input, None, None, None)
