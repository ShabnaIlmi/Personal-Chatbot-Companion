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
    message_placeholder.markdown('<div class="typing-indicator"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>', unsafe_allow_html=True)
    
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
    page_title="Personal AI Assistant",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define a cohesive color scheme
primary_color = "#6C63FF"     # Purple
secondary_color = "#8A84FF"   # Lighter purple
tertiary_color = "#F0EEFF"    # Very light purple
text_color = "#333333"        # Dark gray for text
bg_color = "#FCFCFF"          # Off-white with slight purple tint
accent_color = "#FF9190"      # Soft coral accent

# Inject custom CSS for personal UI
st.markdown(
    f"""
    <style>
        /* Overall app styling */
        .stApp {{
            background-color: {bg_color};
            font-family: 'Poppins', 'Segoe UI', 'Roboto', sans-serif;
        }}
        
        /* Scrollbar styling */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {tertiary_color};
            border-radius: 10px;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {secondary_color};
            border-radius: 10px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: {primary_color};
        }}
        
        /* Header Styling */
        .header-container {{
            text-align: center;
            padding: 20px 0 15px 0;
            margin-bottom: 20px;
            background-color: white;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(108, 99, 255, 0.1);
        }}
        
        .header-title {{
            font-size: 1.8rem;
            font-weight: 700;
            color: {primary_color};
            margin: 0;
        }}
        
        .header-emoji {{
            font-size: 1.8rem;
            margin: 0 5px;
        }}
        
        .header-subtitle {{
            font-size: 0.9rem;
            color: {text_color};
            opacity: 0.8;
            margin-top: 5px;
        }}
        
        /* Stats bar styling */
        .stats-container {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 20px;
            padding: 10px 0;
            border-radius: 12px;
            background-color: white;
            box-shadow: 0 4px 10px rgba(108, 99, 255, 0.1);
        }}
        
        .stat-item {{
            display: flex;
            align-items: center;
            font-size: 0.85rem;
            background-color: {tertiary_color};
            padding: 8px 15px;
            border-radius: 20px;
        }}
        
        .stat-label {{
            margin-right: 5px;
            color: {text_color};
            opacity: 0.7;
        }}
        
        .stat-value {{
            font-weight: 600;
            color: {primary_color};
        }}
        
        /* Chat Container Styling */
        .chat-container {{
            background-color: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(108, 99, 255, 0.1);
            margin-bottom: 20px;
            height: 60vh;
            overflow-y: auto;
        }}
        
        /* User's message styling */
        .user-message {{
            background-color: {primary_color};
            border-radius: 18px 18px 0 18px;
            padding: 12px 16px;
            margin-bottom: 15px;
            font-size: 0.95rem;
            color: white;
            box-shadow: 0 2px 5px rgba(108, 99, 255, 0.2);
            align-self: flex-end;
            max-width: 85%;
            word-wrap: break-word;
            position: relative;
            margin-left: auto;
        }}
        
        /* Assistant's message styling */
        .assistant-message {{
            background-color: {tertiary_color};
            border-radius: 18px 18px 18px 0;
            padding: 12px 16px;
            margin-bottom: 15px;
            font-size: 0.95rem;
            color: {text_color};
            box-shadow: 0 2px 5px rgba(108, 99, 255, 0.1);
            align-self: flex-start;
            max-width: 85%;
            word-wrap: break-word;
            position: relative;
            margin-right: auto;
        }}
        
        /* Message metadata styling */
        .message-metadata {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 6px;
        }}
        
        /* Sender styling */
        .sender {{
            font-weight: 600;
            font-size: 0.85rem;
        }}
        
        .user-sender {{
            color: white;
        }}
        
        .assistant-sender {{
            color: {primary_color};
        }}
        
        /* Timestamp styling */
        .timestamp {{
            font-size: 0.75rem;
        }}
        
        .user-timestamp {{
            color: rgba(255, 255, 255, 0.8);
        }}
        
        .assistant-timestamp {{
            color: rgba(51, 51, 51, 0.6);
        }}
        
        /* Typing indicator */
        .typing-indicator {{
            background-color: {tertiary_color};
            border-radius: 18px 18px 18px 0;
            padding: 15px;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            width: fit-content;
        }}
        
        .typing-indicator .dot {{
            height: 8px;
            width: 8px;
            margin: 0 2px;
            background-color: {primary_color};
            border-radius: 50%;
            opacity: 0.6;
        }}
        
        .typing-indicator .dot:nth-child(1) {{
            animation: bounce 1.2s infinite 0.1s;
        }}
        
        .typing-indicator .dot:nth-child(2) {{
            animation: bounce 1.2s infinite 0.3s;
        }}
        
        .typing-indicator .dot:nth-child(3) {{
            animation: bounce 1.2s infinite 0.5s;
        }}
        
        @keyframes bounce {{
            0%, 100% {{ transform: translateY(0); opacity: 0.6; }}
            50% {{ transform: translateY(-5px); opacity: 0.9; }}
        }}
        
        /* Input area styling */
        .input-container {{
            background-color: white;
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(108, 99, 255, 0.1);
            display: flex;
            align-items: center;
        }}
        
        /* Input Styling */
        .stTextInput input, .stChatInput input {{
            border-radius: 25px !important;
            border: 2px solid {tertiary_color} !important;
            padding: 12px 20px !important;
            font-size: 0.95rem !important;
            color: {text_color} !important;
            box-shadow: none !important;
            transition: all 0.3s ease !important;
        }}
        
        .stTextInput input:focus, .stChatInput input:focus {{
            border-color: {primary_color} !important;
            box-shadow: 0 0 0 2px rgba(108, 99, 255, 0.1) !important;
        }}
        
        /* Footer styling */
        .footer {{
            text-align: center;
            font-size: 0.8rem;
            color: {text_color};
            opacity: 0.7;
            padding: 15px 0;
            margin-top: 20px;
        }}
        
        /* Hide Streamlit branding */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        
        /* Code block styling */
        code {{
            border-radius: 4px;
            padding: 2px 5px;
            background-color: {tertiary_color};
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
            font-size: 0.85em;
            color: {primary_color};
        }}
        
        pre {{
            background-color: {tertiary_color};
            border-radius: 8px;
            padding: 12px;
            overflow-x: auto;
        }}
        
        /* Sidebar styling */
        .css-1cypcdb, .css-163ttbj, .css-1ope8sv {{
            background-color: white;
        }}
        
        .css-pkbazv {{
            color: {primary_color} !important;
        }}
        
        /* Two-column layout for larger screens */
        .main-content {{
            display: flex;
            gap: 20px;
        }}
        
        .chat-column {{
            flex: 7;
        }}
        
        .info-column {{
            flex: 3;
        }}
        
        /* Cards styling */
        .card {{
            background-color: white;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(108, 99, 255, 0.1);
            padding: 15px;
            margin-bottom: 20px;
        }}
        
        .card-header {{
            font-size: 1rem;
            font-weight: 600;
            color: {primary_color};
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 2px solid {tertiary_color};
        }}
        
        /* Features list */
        .features-list {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
        }}
        
        .feature-item {{
            background-color: {tertiary_color};
            padding: 10px;
            border-radius: 8px;
            font-size: 0.85rem;
            color: {text_color};
            display: flex;
            align-items: center;
            transition: transform 0.2s;
        }}
        
        .feature-item:hover {{
            transform: translateY(-3px);
            background-color: rgba(108, 99, 255, 0.1);
        }}
        
        .feature-icon {{
            margin-right: 8px;
            color: {primary_color};
        }}
        
        /* Example prompts */
        .example-prompt {{
            background-color: {tertiary_color};
            padding: 10px 15px;
            border-radius: 8px;
            margin-bottom: 8px;
            font-size: 0.85rem;
            color: {text_color};
            cursor: pointer;
            transition: all 0.2s;
            border-left: 3px solid transparent;
        }}
        
        .example-prompt:hover {{
            border-left: 3px solid {primary_color};
            background-color: rgba(108, 99, 255, 0.1);
        }}
        
        /* Buttons */
        .stButton > button {{
            background-color: {primary_color} !important;
            color: white !important;
            border-radius: 25px !important;
            font-weight: 500 !important;
            border: none !important;
            padding: 10px 25px !important;
            transition: all 0.3s ease !important;
        }}
        
        .stButton > button:hover {{
            background-color: {secondary_color} !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 10px rgba(108, 99, 255, 0.3) !important;
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

# Get current time and date
current_time = datetime.now().strftime("%I:%M %p")
current_date = datetime.now().strftime("%A, %b %d")

# Create a sidebar with additional controls
with st.sidebar:
    st.markdown(f'<div style="text-align: center; padding: 15px 0;"><h3 style="color: {primary_color};">✨ AI Assistant</h3></div>', unsafe_allow_html=True)
    
    # Card for suggested prompts
    st.markdown(
        f'''
        <div class="card">
            <div class="card-header">Try asking me...</div>
            <div class="example-prompts">
                <div class="example-prompt" onclick="selectPrompt('Tell me a fun fact about space')">Tell me a fun fact about space</div>
                <div class="example-prompt" onclick="selectPrompt('What should I cook for dinner?')">What should I cook for dinner?</div>
                <div class="example-prompt" onclick="selectPrompt('Help me plan my weekend')">Help me plan my weekend</div>
                <div class="example-prompt" onclick="selectPrompt('Recommend a book to read')">Recommend a book to read</div>
            </div>
        </div>
        
        <script>
        function selectPrompt(text) {{
            const textareas = parent.document.querySelectorAll('textarea');
            const chatInput = textareas[textareas.length - 1];
            chatInput.value = text;
            chatInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
        }}
        </script>
        ''',
        unsafe_allow_html=True
    )
    
    # Example prompt buttons (fallback for the JS version)
    st.markdown("### Quick Ideas")
    example_prompts = [
        "Tell me a fun fact about space",
        "What should I cook for dinner?",
        "Help me plan my weekend",
        "Recommend a book to read"
    ]
    
    for prompt in example_prompts:
        if st.button(prompt, key=f"btn_{prompt}"):
            st.session_state.prompt_value = prompt
    
    # Card for features
    st.markdown(
        f'''
        <div class="card">
            <div class="card-header">My Capabilities</div>
            <div class="features-list">
                <div class="feature-item">
                    <span class="feature-icon">🧠</span>
                    Answer Questions
                </div>
                <div class="feature-item">
                    <span class="feature-icon">📝</span>
                    Write Content
                </div>
                <div class="feature-item">
                    <span class="feature-icon">💡</span>
                    Creative Ideas
                </div>
                <div class="feature-item">
                    <span class="feature-icon">📚</span>
                    Summarize Text
                </div>
                <div class="feature-item">
                    <span class="feature-icon">🎮</span>
                    Fun & Games
                </div>
                <div class="feature-item">
                    <span class="feature-icon">🧩</span>
                    Solve Problems
                </div>
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )

# Create header section
st.markdown(
    f'''
    <div class="header-container">
        <h1 class="header-title">Personal AI Assistant <span class="header-emoji">✨</span></h1>
        <p class="header-subtitle">Your friendly AI companion powered by Llama 3.3</p>
    </div>
    ''', 
    unsafe_allow_html=True
)

# Stats bar
st.markdown(
    f'''
    <div class="stats-container">
        <div class="stat-item">
            <span class="stat-label">Model:</span>
            <span class="stat-value">Llama 3.3</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Chats:</span>
            <span class="stat-value">{st.session_state.message_count}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Date:</span>
            <span class="stat-value">{current_date}</span>
        </div>
    </div>
    ''',
    unsafe_allow_html=True
)

# Main content area with two columns for larger screens
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Left column - Chat interface
st.markdown('<div class="chat-column">', unsafe_allow_html=True)

# Welcome message when starting a new conversation
if not st.session_state.conversation_started:
    st.session_state.conversation_started = True
    welcome_message = {
        "role": "assistant", 
        "content": "Hi there! 👋 I'm your personal AI assistant. I can help with questions, creative writing, recommendations, and much more. What can I help you with today?",
        "timestamp": current_time
    }
    st.session_state.messages.append(welcome_message)
    st.session_state.message_count += 1

# Create a container for chat messages
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    timestamp = message.get("timestamp", current_time)
    
    if message["role"] == "user":
        st.markdown(
            f'''
            <div class="user-message">
                <div class="message-metadata">
                    <div class="sender user-sender">You</div>
                    <div class="timestamp user-timestamp">{timestamp}</div>
                </div>
                {message["content"]}
            </div>
            ''', 
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'''
            <div class="assistant-message">
                <div class="message-metadata">
                    <div class="sender assistant-sender">AI Assistant</div>
                    <div class="timestamp assistant-timestamp">{timestamp}</div>
                </div>
                {message["content"]}
            </div>
            ''', 
            unsafe_allow_html=True
        )

st.markdown('</div>', unsafe_allow_html=True)

# User Input Section
st.markdown('<div class="input-container">', unsafe_allow_html=True)
prompt = st.chat_input("Ask me anything...", key="chat_input")
st.markdown('</div>', unsafe_allow_html=True)

# Close chat column
st.markdown('</div>', unsafe_allow_html=True)

# Right column content - removed for this personal version for simplicity
st.markdown('</div>', unsafe_allow_html=True)

# Check if there's a prompt value from sidebar buttons
if "prompt_value" in st.session_state and st.session_state.prompt_value:
    prompt = st.session_state.prompt_value
    # Clear the value after using it
    st.session_state.prompt_value = None

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
    
    # Force a rerun to display the updated conversation
    st.rerun()

# Footer
st.markdown(
    f'''
    <div class="footer">
        Personal AI Assistant | Powered by Llama 3.3 via Groq | Made with ❤️
    </div>
    ''', 
    unsafe_allow_html=True
)