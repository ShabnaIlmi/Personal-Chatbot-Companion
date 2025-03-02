from llama_index.llms.groq import Groq
import streamlit as st
import os

# Load API key from Streamlit secrets
api_key = st.secrets["groq"]["api_key"]

# Function to generate chatbot response
def chat_qa(prompt):
    ilm = Groq(model="llama-3.3-70b-versatile", api_key=api_key, temperature=0.5)
    response = ilm.complete(prompt)
    return response

# Define the image path
image_path = os.path.join("assets", "background.jpg")

# Inject custom CSS for background image and UI/UX improvements
st.markdown(
    f"""
    <style>
        /* Background Image Styling */
        .stApp {{
            background-image: url('data:image/jpg;base64,{st.image(image_path, use_column_width=True).getvalue().decode("utf-8")}');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            padding: 0;
        }}

        /* Title Styling */
        .css-18e3th9 {{
            font-family: 'Arial', sans-serif;
            font-size: 2.5em;
            color: #4CAF50;
            text-align: center;
            margin-top: 30px;
        }}

        /* Chat Message Styling */
        .chat-container {{
            max-width: 700px;
            margin: 0 auto;
            background-color: rgba(255, 255, 255, 0.8);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        }}

        /* User's message styling */
        .user-message {{
            background-color: #f1f1f1;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
            font-size: 1.1em;
            color: #333;
        }}

        /* Assistant's message styling */
        .assistant-message {{
            background-color: #d4f7d0;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
            font-size: 1.1em;
            color: #333;
        }}

        /* Input Styling */
        .stTextInput input {{
            font-size: 1.2em;
            border-radius: 15px;
            padding: 10px;
            margin-top: 20px;
        }}

        /* Chatbot input area */
        .stChatInput {{
            background-color: #ffffff;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title(f"*My AI :green[Chatbot]* :sparkles:")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Create a container for chat messages
with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True):
                pass
        else:
            with st.markdown(f'<div class="assistant-message">{message["content"]}</div>', unsafe_allow_html=True):
                pass

    st.markdown('</div>', unsafe_allow_html=True)

# User Input Section
if prompt := st.chat_input("Ask any question here !"):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Get Response from chatbot
    response = chat_qa(prompt)
    
    # Display assistant message
    st.session_state.messages.append({"role": "assistant", "content": response})
