# ai_toolkit.py

import numpy as np
import os
import openai
from colorama import init, Fore, Style
from llama_index import wikipedia_search
from llama_index import write_news_summary
from llama_index import search_news
import json
import warnings
import streamlit as st

is_streamlit = os.getenv("IS_STREAMLIT", False)

if is_streamlit:
    import streamlit as st


with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    # Your code that triggers the warning

openai_api_key = st.secrets["OPENAI_API_KEY"]
newsData_api_key = st.secrets["newsData_api_key"]
openai_api_key = st.secrets["OPENAI_API_KEY"]

api_key = newsData_api_key


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
    api_key = newsData_API
    print(Fore.WHITE + "Staring the country risk tool...")
    country_name = input(Fore.WHITE + "Please confirm the country name: ")
    run_country_analyst_persona(country_name)
  elif 'auditor' in assistant_msg:
    print(Fore.WHITE + "--Starting the auditor tool--")
  elif 'general researcher' in assistant_msg:
    print(Fore.WHITE + "--Starting the default chat model--")
    default_chat(user_input)
  else:
    print(Fore.WHITE + "--Starting the default chat model--")
    default_chat(user_input)

    pass
  

## Default Chat ------------------------------------------------------------------
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

# Country Risk Persona --------------------------------------------
# Gets information for the country and runs the country risk chat
def run_country_analyst_persona(country_name):
    print("Getting Country Data...")
    country_wiki = wikipedia_search(country_name)
    print("Getting Latest News...")
    country_news = search_news(api_key, country_name)
    summarized_news = write_news_summary(country_news)
    print(f"Let's start with some basic information about {country_name}.\nHere's an overview of {country_name} from Wikipedia.")
    print("Wiki here")
    print(f"\nAnd here's the latest news from {country_name}.\n")
    print(summarized_news)
    user_input = (f"I need a detailed country risk assessment for {country_name}.")
    country_risk_chat(user_input, summarized_news, country_wiki, [])

def country_risk_chat(user_input, summarized_news, country_wiki, country_conversation_history):
    country_conversation_history = [
        {"role": "system", "content": "You are an expert geopolitical and security analyst. You produce succinct, insightful country risk assessments looking at both the obvious more subtle factors. Keep your answers short and offer to provide more detail if necessary. Prompt the user for additional context where necessary."},
        {"role": "user", "content": user_input}
    ]
    
    # Prepare system message for this turn
    system_content = ""
    if summarized_news is not None:
        system_content += f"\n{summarized_news}"
    if country_wiki is not None:
        system_content += f"\n{country_wiki[:200]}..."
    if system_content:
        country_conversation_history.append({"role": "system", "content": system_content})

    # Use the assistant_response in the Chat API call
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=country_conversation_history,
        stream=False
    )
    
    assistant_msg = response.choices[0].message['content']
    
    # Append the latest assistant message
    country_conversation_history.append({"role": "assistant", "content": assistant_msg})

    print(Fore.WHITE + assistant_msg)
    print("\n")
    next_user_input = input(Fore.BLUE + "-->")
    country_risk_chat(next_user_input, summarized_news, country_wiki, country_conversation_history)

   
   