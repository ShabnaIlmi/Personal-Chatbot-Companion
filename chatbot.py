from llama_index.llms.groq import Groq
import streamlit as st
import os
import base64
from datetime import datetime
import random

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

# Function to generate dynamic placeholder suggestions
def get_suggestion_placeholder():
    suggestions = [
        "Ask me anything...",
        "What's on your mind?",
        "How can I help you today?",
        "I'm here to assist you...",
        "Tell me what you're looking for...",
        "Looking for answers? Ask away!",
        "Ready for your questions...",
        "Curious about something?",
        "Need help with a task?",
        "Wonder about the universe? Ask me!",
        "Need creative ideas? Let me know!",
        "What would you like to learn today?",
        "Need a hand with something?",
        "Questions or thoughts to share?"
    ]
    return random.choice(suggestions)

# Set page config
st.set_page_config(
    page_title="Personal AI Assistant",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define a more vibrant, fun color scheme
primary_color = "#8A2BE2"     # Vibrant Purple
secondary_color = "#FF6EC7"   # Hot Pink
tertiary_color = "#F0E6FF"    # Light Lavender
text_color = "#333333"        # Dark gray for text
bg_color = "#F8F9FF"          # Soft Blue-White background
accent_color = "#00BFFF"      # Deep Sky Blue accent
gradient_start = "#8A2BE2"    # Purple gradient start
gradient_end = "#FF6EC7"      # Pink gradient end

# Inject custom CSS for personal UI
st.markdown(
    f"""
    <style>
        /* Overall app styling */
        .stApp {{
            background-color: {bg_color};
            font-family: 'Poppins', 'Segoe UI', 'Roboto', sans-serif;
            background-image: radial-gradient(circle at 10% 20%, rgba(138, 43, 226, 0.05) 0%, rgba(255, 110, 199, 0.05) 90%);
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
            padding: 30px 0 25px 0;
            margin-bottom: 30px;
            background: linear-gradient(135deg, {gradient_start}, {gradient_end});
            border-radius: 16px;
            box-shadow: 0 10px 25px rgba(138, 43, 226, 0.3);
            position: relative;
            overflow: hidden;
        }}
        
        .header-container::before {{
            content: "";
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 10%, transparent 10.5%),
                        radial-gradient(circle, rgba(255,255,255,0.1) 10%, transparent 10.5%);
            background-size: 20px 20px;
            background-position: 0 0, 10px 10px;
            transform: rotate(45deg);
            z-index: 1;
        }}
        
        .header-title {{
            font-size: 2.2rem;
            font-weight: 700;
            color: white;
            margin: 0;
            position: relative;
            z-index: 2;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .header-emoji {{
            font-size: 2.2rem;
            margin: 0 5px;
            display: inline-block;
            animation: sparkle 2s infinite;
        }}
        
        @keyframes sparkle {{
            0% {{ transform: scale(1) rotate(0deg); opacity: 1; }}
            25% {{ transform: scale(1.2) rotate(10deg); opacity: 0.8; }}
            50% {{ transform: scale(1) rotate(0deg); opacity: 1; }}
            75% {{ transform: scale(1.2) rotate(-10deg); opacity: 0.8; }}
            100% {{ transform: scale(1) rotate(0deg); opacity: 1; }}
        }}
        
        .header-subtitle {{
            font-size: 1.1rem;
            color: white;
            opacity: 0.9;
            margin-top: 8px;
            position: relative;
            z-index: 2;
        }}
        
        /* Stats bar styling */
        .stats-container {{
            display: flex;
            justify-content: center;
            gap: 25px;
            margin-bottom: 30px;
            padding: 15px;
            border-radius: 12px;
            background-color: white;
            box-shadow: 0 4px 15px rgba(138, 43, 226, 0.15);
        }}

        .stat-item {{
            display: flex;
            align-items: center;
            font-size: 0.95rem;
            background: linear-gradient(135deg, {tertiary_color}, rgba(240, 230, 255, 0.5));
            padding: 10px 18px;
            border-radius: 30px;
            transition: all 0.3s ease;
            border: 1px solid rgba(138, 43, 226, 0.1);
        }}
        
        .stat-item:hover {{
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(138, 43, 226, 0.2);
        }}

        .stat-label {{
            margin-right: 8px;
            color: {text_color};
            opacity: 0.7;
        }}

        .stat-value {{
            font-weight: 600;
            color: {primary_color};
            background: linear-gradient(135deg, {primary_color}, {secondary_color});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
            
        /* Chat Container Styling */
        .chat-container {{
            background-color: white;
            padding: 25px;
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(138, 43, 226, 0.12);
            margin-bottom: 25px;
            height: 60vh;
            overflow-y: auto;
            background-image: 
                radial-gradient(rgba(138, 43, 226, 0.05) 2px, transparent 2px),
                radial-gradient(rgba(255, 110, 199, 0.05) 2px, transparent 2px);
            background-size: 30px 30px;
            background-position: 0 0, 15px 15px;
        }}
        
        /* User's message styling */
        .user-message {{
            background: linear-gradient(135deg, {primary_color}, {secondary_color});
            border-radius: 18px 18px 0 18px;
            padding: 15px 20px;
            margin-bottom: 20px;
            font-size: 1rem;
            color: white;
            box-shadow: 0 5px 15px rgba(138, 43, 226, 0.2);
            align-self: flex-end;
            max-width: 85%;
            word-wrap: break-word;
            position: relative;
            margin-left: auto;
            animation: popIn 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }}
        
        @keyframes popIn {{
            from {{ transform: scale(0.8); opacity: 0; }}
            to {{ transform: scale(1); opacity: 1; }}
        }}
        
        /* Assistant's message styling */
        .assistant-message {{
            background: linear-gradient(135deg, {tertiary_color}, rgba(240, 230, 255, 0.7));
            border-radius: 18px 18px 18px 0;
            padding: 15px 20px;
            margin-bottom: 20px;
            font-size: 1rem;
            color: {text_color};
            box-shadow: 0 5px 15px rgba(138, 43, 226, 0.1);
            align-self: flex-start;
            max-width: 85%;
            word-wrap: break-word;
            position: relative;
            margin-right: auto;
            animation: slideUp 0.3s ease-out;
            border-left: 3px solid {primary_color};
        }}
        
        @keyframes slideUp {{
            from {{ transform: translateY(10px); opacity: 0; }}
            to {{ transform: translateY(0); opacity: 1; }}
        }}
        
        /* Message metadata styling */
        .message-metadata {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        
        /* Sender styling */
        .sender {{
            font-weight: 600;
            font-size: 0.9rem;
        }}
        
        .user-sender {{
            color: white;
        }}
        
        .assistant-sender {{
            background: linear-gradient(135deg, {primary_color}, {secondary_color});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
        }}
        
        .assistant-sender::before {{
            content: "✨";
            margin-right: 5px;
            font-size: 0.85rem;
        }}
        
        /* Timestamp styling */
        .timestamp {{
            font-size: 0.8rem;
            font-style: italic;
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
            padding: 20px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            width: fit-content;
        }}
        
        .typing-indicator .dot {{
            height: 10px;
            width: 10px;
            margin: 0 3px;
            background: linear-gradient(135deg, {primary_color}, {secondary_color});
            border-radius: 50%;
            opacity: 0.8;
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
            0%, 100% {{ transform: translateY(0); opacity: 0.8; }}
            50% {{ transform: translateY(-8px); opacity: 1; }}
        }}
        
        /* Input area styling */
        .input-container {{
            background-color: white;
            padding: 20px;
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(138, 43, 226, 0.12);
            display: flex;
            align-items: center;
            position: relative;
        }}
        
        /* Input Styling */
        .stTextInput input, .stChatInput input {{
            border-radius: 50px !important;
            border: 2px solid {tertiary_color} !important;
            padding: 15px 25px !important;
            font-size: 1rem !important;
            color: {text_color} !important;
            box-shadow: none !important;
            transition: all 0.3s ease !important;
        }}
        
        .stTextInput input:focus, .stChatInput input:focus {{
            border-color: {primary_color} !important;
            box-shadow: 0 0 0 5px rgba(138, 43, 226, 0.1) !important;
            transform: translateY(-2px) !important;
        }}
        
        /* Footer styling */
        .footer {{
            text-align: center;
            font-size: 0.9rem;
            color: {text_color};
            opacity: 0.7;
            padding: 20px 0;
            margin-top: 30px;
            position: relative;
        }}
        
        .footer::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 2px;
            background: linear-gradient(to right, transparent, {primary_color}, {secondary_color}, transparent);
        }}
        
        /* Hide Streamlit branding */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        
        /* Code block styling */
        code {{
            border-radius: 4px;
            padding: 3px 6px;
            background-color: {tertiary_color};
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
            font-size: 0.9em;
            color: {primary_color};
        }}
        
        pre {{
            background-color: {tertiary_color};
            border-radius: 8px;
            padding: 15px;
            overflow-x: auto;
            box-shadow: inset 0 0 5px rgba(0,0,0,0.05);
        }}
        
        /* Remove the two-column layout causing the white box */
        
        /* Cards styling */
        .card {{
            background-color: white;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(138, 43, 226, 0.1);
            padding: 15px;
            margin-bottom: 20px;
        }}
        
        .card-header {{
            font-size: 1rem;
            font-weight: 600;
            background: linear-gradient(135deg, {primary_color}, {secondary_color});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 2px solid {tertiary_color};
        }}
        
        /* Buttons */
        .stButton > button {{
            background: linear-gradient(135deg, {primary_color}, {secondary_color}) !important;
            color: white !important;
            border-radius: 25px !important;
            font-weight: 500 !important;
            border: none !important;
            padding: 10px 25px !important;
            transition: all 0.3s ease !important;
        }}
        
        .stButton > button:hover {{
            background: linear-gradient(135deg, {secondary_color}, {primary_color}) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 10px rgba(138, 43, 226, 0.3) !important;
        }}
        
        /* Enhanced animations */
        .user-message, .assistant-message {{
            animation: fadeIn 0.3s ease-in-out;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        /* Example prompt styling */
        .example-prompts {{
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-top: 10px;
        }}
        
        .example-prompt {{
            background-color: {tertiary_color};
            padding: 10px 15px;
            border-radius: 8px;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.2s ease;
            border-left: 3px solid {primary_color};
        }}
        
        .example-prompt:hover {{
            background-color: rgba(240, 230, 255, 0.8);
            transform: translateX(3px);
            box-shadow: 0 2px 5px rgba(138, 43, 226, 0.1);
        }}
        
        /* Features list styling */
        .features-list {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-top: 10px;
        }}
        
        .feature-item {{
            display: flex;
            align-items: center;
            gap: 5px;
            font-size: 0.9rem;
        }}
        
        .feature-icon {{
            font-size: 1.1rem;
        }}
        
        /* Try asking me feature styling */
        .try-asking-container {{
            background: linear-gradient(135deg, rgba(138, 43, 226, 0.05), rgba(255, 110, 199, 0.05));
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 30px;
            border: 1px solid rgba(138, 43, 226, 0.1);
            box-shadow: 0 5px 15px rgba(138, 43, 226, 0.08);
        }}
        
        .try-asking-title {{
            font-size: 1.2rem;
            margin-bottom: 15px;
            color: {primary_color};
            font-weight: 600;
        }}
        
        .suggestions-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
        }}
        
        .suggestion-item {{
            background: white;
            padding: 12px 15px;
            border-radius: 10px;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.2s ease;
            border-left: 3px solid {secondary_color};
            box-shadow: 0 2px 5px rgba(138, 43, 226, 0.08);
        }}
        
        .suggestion-item:hover {{
            background-color: {tertiary_color};
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(138, 43, 226, 0.15);
        }}
        
        /* Animated placeholder text */
        .animated-placeholder {{
            font-size: 1rem;
            color: rgba(138, 43, 226, 0.6);
            animation: fadeIn 2s infinite alternate;
            display: block;
            margin: 10px 0;
            padding: 10px 20px;
            background: rgba(240, 230, 255, 0.5);
            border-radius: 8px;
            text-align: center;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0.6; }}
            to {{ opacity: 1; }}
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
if "current_suggestion" not in st.session_state:
    st.session_state.current_suggestion = get_suggestion_placeholder()

# Get current time and date
current_time = datetime.now().strftime("%I:%M %p")
current_date = datetime.now().strftime("%A, %b %d")

# Create a sidebar with additional controls
with st.sidebar:
    st.markdown(f'<div style="text-align: center; padding: 15px 0;"><h3 style="color: {primary_color};">✨ AI Assistant</h3></div>', unsafe_allow_html=True)
    
    # Example prompts without JavaScript dependency
    st.markdown("<div class='card'><div class='card-header'>Try asking me...</div></div>", unsafe_allow_html=True)
    
    example_prompts = [
        "Tell me a fun fact about space",
        "What should I cook for dinner?",
        "Help me plan my weekend",
        "Recommend a book to read"
    ]
    
    # Create buttons that look like the prompt examples
    for i, prompt in enumerate(example_prompts):
        if st.button(prompt, key=f"prompt_{i}"):
            st.session_state.user_prompt = prompt
    
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

# New "Try asking me" section before the chat
if not st.session_state.messages:
    st.markdown(
        f'''
        <div class="try-asking-container">
            <div class="try-asking-title">✨ Try asking me about...</div>
            <div class="suggestions-grid">
                <div class="suggestion-item" onclick="document.querySelector('.stChatInput input').value = 'How do black holes work?'; document.querySelector('.stChatInput button').click();">
                    How do black holes work?
                </div>
                <div class="suggestion-item" onclick="document.querySelector('.stChatInput input').value = 'Write a short poem about autumn'; document.querySelector('.stChatInput button').click();">
                    Write a short poem about autumn
                </div>
                <div class="suggestion-item" onclick="document.querySelector('.stChatInput input').value = 'Give me a healthy breakfast recipe'; document.querySelector('.stChatInput button').click();">
                    Give me a healthy breakfast recipe
                </div>
                <div class="suggestion-item" onclick="document.querySelector('.stChatInput input').value = 'Explain quantum computing simply'; document.querySelector('.stChatInput button').click();">
                    Explain quantum computing simply
                </div>
                <div class="suggestion-item" onclick="document.querySelector('.stChatInput input').value = 'Help me draft an email to request time off'; document.querySelector('.stChatInput button').click();">
                    Help me draft an email to request time off
                </div>
                <div class="suggestion-item" onclick="document.querySelector('.stChatInput input').value = 'Tell me an interesting historical fact'; document.querySelector('.stChatInput button').click();">
                    Tell me an interesting historical fact
                </div>
            </div>
            
            <div class="animated-placeholder">
                {st.session_state.current_suggestion}
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )

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

# Update the placeholder text for the chat input field
st.session_state.current_suggestion = get_suggestion_placeholder()

# User Input Section
st.markdown('<div class="input-container">', unsafe_allow_html=True)
prompt = st.chat_input(st.session_state.current_suggestion, key="chat_input")
st.markdown('</div>', unsafe_allow_html=True)

# Check if there's a prompt value from sidebar buttons
if "user_prompt" in st.session_state and st.session_state.user_prompt:
    prompt = st.session_state.user_prompt
    # Clear the value after using it
    st.session_state.user_prompt = None

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
    
    # Update the placeholder for next time
    st.session_state.current_suggestion = get_suggestion_placeholder()
    
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