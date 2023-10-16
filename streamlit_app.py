#streamlit_app code

import streamlit as st
from start import start  # Import your existing functions/modules

# Initialize session state for conversation history
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Your greeting and initial setup
st.write("Streamlit is opening the risk management copilot")

# ... other Streamlit setup like date, warnings, etc.

# Text input for user message
user_input = st.text_input("You: ")

# Button to send message
send_button = st.button("Send")

# Display and handle chat
if send_button:
    # Append user's message to conversation history
    st.session_state.conversation_history.append({"role": "user", "content": user_input})

    # Check user intent or route task
    system_response, additional_info = start(user_input)  # Replace with your existing logic

    # Append system's message to conversation history
    st.session_state.conversation_history.append({"role": "system", "content": system_response})

# Display the conversation history in Streamlit
for message in st.session_state.conversation_history:
    if message["role"] == "user":
        st.write(f"You: {message['content']}")
    else:
        st.write(f"System: {message['content']}")
