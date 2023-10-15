##main.py


# Test bed for the main AI ERM components
from utilities import Spinner
import time
from ai_toolkit import task_routing
from ai_toolkit import default_chat
from utilities import check_intent
import datetime
from colorama import init, Fore, Style
import warnings

init()

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    # Your code that triggers the warning

now = datetime.datetime.now()
now_formatted = now.strftime("%b-%d-%Y %H:%M")
print('Welcome to the risk management copilot')
with Spinner("Loading"):
    time.sleep(2)
print("\nFired up and ready to go\n")
print(Fore.YELLOW + """Hi, I'm your risk managementcopilot, here to assist you with risk, security and crisis tasks.\n
Every thing we do is via this chat interface but there's an extensive toolkit that I can deploy for you. This includes: country risk analysis, enterprise risk assessment, crisis preparadness and ERM compliance. There is also general chat and web search available.\n
**Note**
To make sure I am using the right tool for the job, I will periodically check that we are on the right track. Please correct me if I am going in the wrong direction. If you need to switch focus, e.g. from country risk to contigency planning, simply write 'SWITCH FOCUS' and I'll reorientate.\n
Let's get started.\n""")

print("Please enter your name so we can get started")
user_name = input(Fore.BLUE + "-->")

check_intent(user_name)

print(Fore.GREEN + f"\nLatest update as of {now_formatted}:\nTask routing component functioning. \nEnd of demo.")

