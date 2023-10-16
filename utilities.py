# utilities.py

import itertools
import threading
import time
from ai_toolkit import task_routing
from colorama import init, Fore, Style
import json
import os

is_streamlit = os.getenv("IS_STREAMLIT", False)

if is_streamlit:
    import streamlit as st


#Makes a loading spinner
class Spinner:
    def __init__(self, message):
        self.spinner_chars = itertools.cycle(['-', '/', '|', '\\'])
        self.is_active = False
        self.message = message

    def __enter__(self):
        self.is_active = True
        self.spinner_thread = threading.Thread(target=self.spin)
        self.spinner_thread.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.is_active = False
        self.spinner_thread.join()

    def spin(self):
        while self.is_active:
            print(f"\r{next(self.spinner_chars)} {self.message}", end='')
            time.sleep(0.1)


# Checks the user intent to select the right model to use
def check_intent(user_name):
  if is_streamlit:
      user_input = st.text_input(f"What can I help you with {user_name}?")
      task_routing(user_input)
    else:
        print(Fore.WHITE + f"What can I help you with {user_name}?")
        user_input = input(Fore.BLUE + "-->")
        task_routing(user_input)



