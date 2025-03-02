from llama_index.llms.groq import Groq
import streamlit as st
import os
import base64
from datetime import datetime

# Load API key from Streamlit secrets
api_key = st.secrets["groq"]["api_key"]

# Function to generate chatbot response
def chat_qa(prompt):
    # Add a typing indicator
    message_placeholder = st.empty()
    message_placeholder.markdown('<div class="typing-indicator"><span></span><span></span><span></span></div>', unsafe_allow_html=True)
    
    # Get response from Groq
    ilm = Groq(model="llama-3.3-70b-versatile", api_key=api_key, temperature=0.5)
    response = ilm.complete(prompt)
    
    # Remove typing indicator
    message_placeholder.empty()
    
    return response

# Function to encode image to base64
def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Set page config
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Try to get background image - with fallback
try:
    # Define the image path - updated to correct folder structure
    image_path = os.path.join("assets", "images", "background.jpg")
    # Get base64 encoded image
    img_data = get_base64_encoded_image(image_path)
    background_style = f"""
    background-image: url('data:image/jpg;base64,{img_data}');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    """
except Exception as e:
    # Fallback to a premium gradient background if image loading fails
    background_style = """
    background: linear-gradient(135deg, #1a2a6c 0%, #b21f1f 50%, #fdbb2d 100%);
    """

# Define theme colors (can be customized)
primary_color = "#4CAF50"
secondary_color = "#2E7D32"
accent_color = "#81C784"
text_color = "#333333"
light_bg = "rgba(255, 255, 255, 0.92)"

# Inject custom CSS for enhanced UI/UX
st.markdown(
    f"""
    <style>
        /* Background Styling */
        .stApp {{
            {background_style}
            padding: 0;
        }}
        
        /* Scrollbar styling */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {primary_color};
            border-radius: 10px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: {secondary_color};
        }}
        
        /* Title Styling */
        .title-container {{
            text-align: center;
            padding: 20px 0;
            margin-bottom: 20px;
            background-color: {light_bg};
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(5px);
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
            border-left: 5px solid {primary_color};
            border-right: 5px solid {primary_color};
        }}
        
        .title-text {{
            font-family: 'Poppins', 'Arial', sans-serif;
            font-size: 2.5em;
            color: {primary_color};
            margin: 0;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }}
        
        .subtitle-text {{
            font-family: 'Poppins', 'Arial', sans-serif;
            font-size: 1.2em;
            color: {text_color};
            margin-top: 5px;
            opacity: 0.8;
        }}
        
        /* Chat Container Styling */
        .chat-container {{
            max-width: 800px;
            margin: 0 auto 20px auto;
            background-color: {light_bg};
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(5px);
            min-height: 400px;
            max-height: 600px;
            overflow-y: auto;
            border-left: 5px solid {primary_color};
            border-right: 5px solid {primary_color};
            display: flex;
            flex-direction: column;
        }}
        
        /* User's message styling */
        .user-message {{
            background-color: #f1f1f1;
            border-radius: 18px 18px 0 18px;
            padding: 12px 18px;
            margin-bottom: 15px;
            font-size: 1.1em;
            color: {text_color};
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
            align-self: flex-end;
            max-width: 80%;
            word-wrap: break-word;
            position: relative;
            margin-left: auto;
            border-top: 1px solid #e0e0e0;
            animation: slideInRight 0.3s ease-out forwards;
        }}
        
        @keyframes slideInRight {{
            from {{ transform: translateX(20px); opacity: 0; }}
            to {{ transform: translateX(0); opacity: 1; }}
        }}
        
        /* Assistant's message styling */
        .assistant-message {{
            background-color: #e8f5e9;
            border-radius: 18px 18px 18px 0;
            padding: 12px 18px;
            margin-bottom: 15px;
            font-size: 1.1em;
            color: {text_color};
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
            align-self: flex-start;
            max-width: 80%;
            word-wrap: break-word;
            position: relative;
            margin-right: auto;
            border-top: 1px solid #c8e6c9;
            animation: slideInLeft 0.3s ease-out forwards;
        }}
        
        @keyframes slideInLeft {{
            from {{ transform: translateX(-20px); opacity: 0; }}
            to {{ transform: translateX(0); opacity: 1; }}
        }}
        
        /* Timestamp styling */
        .timestamp {{
            font-size: 0.75em;
            color: #757575;
            margin-top: 5px;
            text-align: right;
        }}
        
        /* Message sender styling */
        .sender {{
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        /* Typing indicator */
        .typing-indicator {{
            background-color: #e8f5e9;
            border-radius: 18px 18px 18px 0;
            padding: 15px 20px;
            display: inline-block;
            margin-bottom: 15px;
            position: relative;
            animation: slideInLeft 0.3s ease-out forwards;
            align-self: flex-start;
        }}
        
        .typing-indicator span {{
            height: 10px;
            width: 10px;
            float: left;
            margin: 0 1px;
            background-color: {primary_color};
            display: block;
            border-radius: 50%;
            opacity: 0.4;
        }}
        
        .typing-indicator span:nth-of-type(1) {{
            animation: 1s blink infinite 0.3333s;
        }}
        
        .typing-indicator span:nth-of-type(2) {{
            animation: 1s blink infinite 0.6666s;
        }}
        
        .typing-indicator span:nth-of-type(3) {{
            animation: 1s blink infinite 0.9999s;
        }}
        
        @keyframes blink {{
            50% {{ opacity: 1; }}
        }}
        
        /* Input area styling */
        .input-container {{
            max-width: 800px;
            margin: 0 auto;
            background-color: {light_bg};
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(5px);
            display: flex;
            align-items: center;
            border-left: 5px solid {primary_color};
            border-right: 5px solid {primary_color};
        }}
        
        /* Input Styling */
        .stTextInput input, .stChatInput input {{
            font-size: 1.2em;
            border-radius: 25px !important;
            padding: 12px 20px !important;
            border: 2px solid {primary_color} !important;
            width: 100%;
            transition: all 0.3s ease;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        }}
        
        .stTextInput input:focus, .stChatInput input:focus {{
            border-color: {secondary_color} !important;
            box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2) !important;
        }}
        
        /* Custom button styling */
        .stButton > button {{
            background-color: {primary_color};
            color: white;
            font-weight: bold;
            border-radius: 25px;
            padding: 12px 25px;
            border: none;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 10px;
        }}
        
        .stButton > button:hover {{
            background-color: {secondary_color};
            box-shadow: 0 4px 15px rgba(46, 125, 50, 0.4);
            transform: translateY(-2px);
        }}
        
        /* Info cards */
        .info-container {{
            display: flex;
            justify-content: space-between;
            max-width: 800px;
            margin: 0 auto 20px auto;
            gap: 15px;
        }}
        
        .info-card {{
            background-color: {light_bg};
            border-radius: 10px;
            padding: 15px;
            flex: 1;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(5px);
            text-align: center;
            border-top: 3px solid {primary_color};
            transition: transform 0.3s ease;
        }}
        
        .info-card:hover {{
            transform: translateY(-5px);
        }}
        
        .info-card-title {{
            font-weight: bold;
            margin-bottom: 5px;
            color: {primary_color};
        }}
        
        .info-card-value {{
            font-size: 1.2em;
            color: {text_color};
        }}
        
        /* Footer styling */
        .footer {{
            text-align: center;
            margin-top: 30px;
            font-size: 0.9em;
            color: rgba(255, 255, 255, 0.8);
            padding: 10px;
        }}
        
        /* Hide Streamlit branding */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        
        /* Emoji animations */
        .emoji {{
            display: inline-block;
            animation: wave 1.8s infinite;
        }}
        
        @keyframes wave {{
            0% {{ transform: rotate(0deg); }}
            10% {{ transform: rotate(14deg); }}
            20% {{ transform: rotate(-8deg); }}
            30% {{ transform: rotate(14deg); }}
            40% {{ transform: rotate(-4deg); }}
            50% {{ transform: rotate(10deg); }}
            60% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(0deg); }}
        }}
        
        /* Code block styling */
        code {{
            border-radius: 5px;
            padding: 2px 5px;
            background-color: rgba(0, 0, 0, 0.05);
            font-family: 'Courier New', monospace;
        }}
        
        pre {{
            background-color: rgba(0, 0, 0, 0.05);
            border-radius: 5px;
            padding: 10px;
            overflow-x: auto;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_started" not in st.session_state:
    st.session_state.conversation_started = False
if "message_count" not in st.session_state:
    st.session_state.message_count = 0

# Custom title with HTML
st.markdown(
    '''
    <div class="title-container">
        <h1 class="title-text">AI Assistant <span class="emoji">🤖</span></h1>
        <p class="subtitle-text">Your intelligent conversation partner powered by Groq</p>
    </div>
    ''', 
    unsafe_allow_html=True
)

# Display stats cards
st.markdown(
    f'''
    <div class="info-container">
        <div class="info-card">
            <div class="info-card-title">Model</div>
            <div class="info-card-value">Llama-3.3-70B</div>
        </div>
        <div class="info-card">
            <div class="info-card-title">Messages</div>
            <div class="info-card-value">{st.session_state.message_count}</div>
        </div>
        <div class="info-card">
            <div class="info-card-title">Temperature</div>
            <div class="info-card-value">0.5</div>
        </div>
    </div>
    ''',
    unsafe_allow_html=True
)

# Welcome message when starting a new conversation
if not st.session_state.conversation_started:
    st.session_state.conversation_started = True
    current_time = datetime.now().strftime("%I:%M %p")
    welcome_message = {
        "role": "assistant", 
        "content": "Hello! I'm your AI assistant powered by Llama 3.3. How can I help you today?",
        "timestamp": current_time
    }
    st.session_state.messages.append(welcome_message)
    st.session_state.message_count += 1

# Create a container for chat messages
with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display chat messages
    for message in st.session_state.messages:
        timestamp = message.get("timestamp", datetime.now().strftime("%I:%M %p"))
        
        if message["role"] == "user":
            st.markdown(
                f'''
                <div class="user-message">
                    <div class="sender">You</div>
                    {message["content"]}
                    <div class="timestamp">{timestamp}</div>
                </div>
                ''', 
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'''
                <div class="assistant-message">
                    <div class="sender">Assistant</div>
                    {message["content"]}
                    <div class="timestamp">{timestamp}</div>
                </div>
                ''', 
                unsafe_allow_html=True
            )
    
    st.markdown('</div>', unsafe_allow_html=True)

# User Input Section (wrapped in a container for styling)
st.markdown('<div class="input-container">', unsafe_allow_html=True)
prompt = st.chat_input("Ask me anything...")
st.markdown('</div>', unsafe_allow_html=True)

if prompt:
    # Get current time
    current_time = datetime.now().strftime("%I:%M %p")
    
    # Display user message
    st.session_state.messages.append({
        "role": "user", 
        "content": prompt,
        "timestamp": current_time
    })
    st.session_state.message_count += 1
    
    # Get Response from chatbot
    response = chat_qa(prompt)
    
    # Display assistant message
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response,
        "timestamp": datetime.now().strftime("%I:%M %p")
    })
    st.session_state.message_count += 1
    
    # Removed experimental_rerun() - Streamlit will automatically rerun
    # when the session state changes

# Footer
st.markdown(
    '''
    <div class="footer">
        Powered by Groq | Llama-3.3-70B | Created with ❤️ using Streamlit
    </div>
    ''', 
    unsafe_allow_html=True
)