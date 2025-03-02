from llama_index.llms.groq import Groq
import streamlit as st
import os
import base64

# Load API key from Streamlit secrets
api_key = st.secrets["groq"]["api_key"]

# Function to generate chatbot response
def chat_qa(prompt):
    ilm = Groq(model="llama-3.3-70b-versatile", api_key=api_key, temperature=0.5)
    response = ilm.complete(prompt)
    return response

# Function to encode image to base64
def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Try to get background image - with fallback
try:
    # Define the image path
    image_path = os.path.join("assets", "background.jpg")
    # Get base64 encoded image
    img_data = get_base64_encoded_image(image_path)
    background_style = f"""
    background-image: url('data:image/jpg;base64,{img_data}');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    """
except Exception:
    # Fallback to a gradient background if image loading fails
    background_style = """
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    """

# Inject custom CSS for background and UI improvements
st.markdown(
    f"""
    <style>
        /* Background Styling */
        .stApp {{
            {background_style}
            padding: 0;
        }}
        
        /* Title Styling */
        .title-container {{
            text-align: center;
            padding: 20px 0;
            margin-bottom: 20px;
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
        }}
        
        .title-text {{
            font-family: 'Arial', sans-serif;
            font-size: 2.5em;
            color: #4CAF50;
            margin: 0;
        }}
        
        /* Chat Message Styling */
        .chat-container {{
            max-width: 700px;
            margin: 0 auto;
            background-color: rgba(255, 255, 255, 0.85);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        }}
        
        /* User's message styling */
        .user-message {{
            background-color: #f1f1f1;
            border-radius: 10px;
            padding: 12px;
            margin-bottom: 15px;
            font-size: 1.1em;
            color: #333;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }}
        
        /* Assistant's message styling */
        .assistant-message {{
            background-color: #d4f7d0;
            border-radius: 10px;
            padding: 12px;
            margin-bottom: 15px;
            font-size: 1.1em;
            color: #333;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }}
        
        /* Input Styling */
        .stTextInput input, .stChatInput input {{
            font-size: 1.2em;
            border-radius: 15px !important;
            padding: 10px;
            margin-top: 20px;
            border: 2px solid #4CAF50 !important;
        }}
        
        /* Custom button styling */
        .stButton > button {{
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px 20px;
            border: none;
            transition: all 0.3s ease;
        }}
        
        .stButton > button:hover {{
            background-color: #3e8e41;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Custom title with HTML
st.markdown('<div class="title-container"><h1 class="title-text">My AI Chatbot ✨</h1></div>', unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Create a container for chat messages
with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="assistant-message">{message["content"]}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# User Input Section
prompt = st.chat_input("Ask any question here!")
if prompt:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Get Response from chatbot
    response = chat_qa(prompt)
    
    # Display assistant message
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Force a rerun to display the new messages
    st.experimental_rerun()