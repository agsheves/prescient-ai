import numpy as np
import os
import openai
from colorama import init, Fore, Style
from llamaindex import wikipedia_search
from llamaindex import get_country_news
init()

from secret_files.secret_keys import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY
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
    country_news = get_country_news(country_name)
    country_risk_chat(user_input, country_news, country_wiki)
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

def country_risk_chat(user_input, country_news, country_wiki):
  global country_conversation_history  # Access the global conversation history
  country_conversation_history.append({"role": "user", "content": user_input})


  if country_news:
    country_conversation_history.append({"role": "assistant", "content": country_news})
  if country_wiki:
    country_conversation_history.append({"role": "assistant", "content": country_wiki})

  response = openai.ChatCompletion.create(
      model="gpt-4",
      messages=country_conversation_history,
      stream=False
  )

  assistant_msg = response.choices[0].message['content']
  country_conversation_history.append({"role": "assistant", "content": assistant_msg})

  print(Fore.WHITE + assistant_msg)
  print("\n")
  user_input = input(Fore.BLUE + "-->")
  country_risk_chat(user_input, None, None)  # Pass None for country_wiki during subsequent chat interactions
