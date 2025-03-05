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
    
    # Convert response to string if it's not already
    if hasattr(response, 'text'):
        return response.text
    elif not isinstance(response, str):
        return str(response)
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
        
        /* Scrollbar styling - global */
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
        
        /* Sidebar enhancements */
        .css-1d391kg, .css-163ttbj, .css-1wrcr25 {{
            background-image: linear-gradient(170deg, {primary_color}22, {secondary_color}22);
            border-right: 1px solid rgba(138, 43, 226, 0.1);
        }}
        
        /* Sidebar header */
        .sidebar-header {{
            background: linear-gradient(135deg, {gradient_start}, {gradient_end});
            margin: -1rem -1rem 1rem -1rem;
            padding: 2rem 1rem;
            border-radius: 0 0 20px 0;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            position: relative;
            overflow: hidden;
        }}
        
        .sidebar-header::before {{
            content: "";
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 10%, transparent 10.5%);
            background-size: 20px 20px;
            transform: rotate(45deg);
            z-index: 1;
            opacity: 0.5;
        }}
        
        .sidebar-title {{
            font-size: 1.5rem;
            font-weight: 700;
            color: white;
            margin: 0;
            position: relative;
            z-index: 2;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }}
        
        /* Sidebar card styling */
        .sidebar-card {{
            background-color: white;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 8px 20px rgba(138, 43, 226, 0.1);
            border-left: 4px solid {primary_color};
            transition: transform 0.3s ease;
        }}
        
        .sidebar-card:hover {{
            transform: translateY(-3px);
        }}
        
        .sidebar-card-header {{
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid {tertiary_color};
            color: {primary_color};
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        /* Example prompt styling */
        .example-prompts {{
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}
        
        .example-prompt {{
            background: linear-gradient(135deg, {tertiary_color}, rgba(240, 230, 255, 0.5));
            padding: 12px 18px;
            border-radius: 12px;
            font-size: 0.95rem;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 2px 5px rgba(138, 43, 226, 0.05);
            border: 1px solid rgba(138, 43, 226, 0.08);
            position: relative;
            padding-left: 25px;
        }}
        
        .example-prompt::before {{
            content: "💬";
            position: absolute;
            left: 10px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 0.8rem;
        }}
        
        .example-prompt:hover {{
            background: linear-gradient(135deg, {tertiary_color}, white);
            transform: translateX(5px);
            box-shadow: 0 5px 10px rgba(138, 43, 226, 0.1);
        }}
        
        /* Features list styling */
        .features-list {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 12px;
        }}
        
        .feature-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 0.95rem;
            background-color: white;
            padding: 12px 15px;
            border-radius: 12px;
            transition: all 0.3s ease;
            border-left: 3px solid {primary_color};
        }}
        
        .feature-item:hover {{
            transform: translateX(5px);
            background-color: {tertiary_color};
        }}
        
        .feature-icon {{
            font-size: 1.2rem;
            background: linear-gradient(135deg, {primary_color}, {secondary_color});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        /* Capabilities Grid Styling */
        .features-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-top: 10px;
        }}

        .capability-tile {{
            background: linear-gradient(135deg, #F0E6FF, rgba(240, 230, 255, 0.5));
            border-radius: 12px;
            padding: 15px 10px;
            display: flex;
            flex-direction: column;
            align-items: center;
            transition: all 0.3s ease;
            border-left: 3px solid #8A2BE2;
            cursor: pointer;
        }}

        .capability-tile:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(138, 43, 226, 0.15);
            background: linear-gradient(135deg, #F0E6FF, white);
        }}

        .capability-icon {{
            font-size: 1.5rem;
            margin-bottom: 8px;
        }}

        .capability-text {{
            font-size: 0.85rem;
            font-weight: 500;
            color: #333333;
            text-align: center;
        }}
        
        .feature-text {{
            color: {text_color};
        }}
        
        /* Header Styling */
        .header-container {{
            text-align: center;
            padding: 35px 0 30px 0;
            margin-bottom: 35px;
            background: linear-gradient(135deg, {gradient_start}, {gradient_end});
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(138, 43, 226, 0.3);
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
            font-size: 2.5rem;
            font-weight: 800;
            color: white;
            margin: 0;
            position: relative;
            z-index: 2;
            text-shadow: 0 3px 6px rgba(0,0,0,0.2);
        }}
        
        .header-emoji {{
            font-size: 2.5rem;
            margin: 0 8px;
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
            font-size: 1.2rem;
            color: white;
            opacity: 0.9;
            margin-top: 10px;
            position: relative;
            z-index: 2;
        }}
        
        /* Stats bar styling */
        .stats-container {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-bottom: 35px;
            padding: 5px;
            border-radius: 16px;
            background-color: white;
            box-shadow: 0 8px 25px rgba(138, 43, 226, 0.15);
            position: relative;
            transform: translateY(-25px);
        }}

        .stat-item {{
            display: flex;
            align-items: center;
            font-size: 1rem;
            background: linear-gradient(135deg, {tertiary_color}, rgba(240, 230, 255, 0.5));
            padding: 15px 25px;
            border-radius: 30px;
            transition: all 0.3s ease;
            border: 1px solid rgba(138, 43, 226, 0.1);
        }}
        
        .stat-item:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(138, 43, 226, 0.2);
        }}

        .stat-label {{
            margin-right: 10px;
            color: {text_color};
            opacity: 0.7;
            font-weight: 500;
        }}

        .stat-value {{
            font-weight: 700;
            color: {primary_color};
            background: linear-gradient(135deg, {primary_color}, {secondary_color});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
            
        /* Chat Container Styling */
        .chat-container {{
            background-color: white;
            padding: 30px;
            border-radius: 24px;
            box-shadow: 0 15px 40px rgba(138, 43, 226, 0.12);
            margin-bottom: 30px;
            height: 60vh;
            overflow-y: auto;
            background-image: 
                radial-gradient(rgba(138, 43, 226, 0.05) 2px, transparent 2px),
                radial-gradient(rgba(255, 110, 199, 0.05) 2px, transparent 2px);
            background-size: 30px 30px;
            background-position: 0 0, 15px 15px;
            position: relative;
        }}
        
        .chat-container::after {{
            content: "";
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 60px;
            background: linear-gradient(to top, white, transparent);
            pointer-events: none;
            z-index: 1;
            border-radius: 0 0 24px 24px;
        }}
        
        /* User's message styling */
        .user-message {{
            background: linear-gradient(135deg, {primary_color}, {secondary_color});
            border-radius: 22px 22px 0 22px;
            padding: 18px 25px;
            margin-bottom: 25px;
            font-size: 1.05rem;
            color: white;
            box-shadow: 0 8px 20px rgba(138, 43, 226, 0.2);
            align-self: flex-end;
            max-width: 85%;
            word-wrap: break-word;
            position: relative;
            margin-left: auto;
            animation: popIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }}
        
        @keyframes popIn {{
            from {{ transform: scale(0.8); opacity: 0; }}
            to {{ transform: scale(1); opacity: 1; }}
        }}
        
        /* Assistant's message styling */
        .assistant-message {{
            background: linear-gradient(135deg, {tertiary_color}, rgba(240, 230, 255, 0.7));
            border-radius: 22px 22px 22px 0;
            padding: 18px 25px;
            margin-bottom: 25px;
            font-size: 1.05rem;
            line-height: 1.6;
            color: {text_color};
            box-shadow: 0 8px 20px rgba(138, 43, 226, 0.1);
            align-self: flex-start;
            max-width: 85%;
            word-wrap: break-word;
            position: relative;
            margin-right: auto;
            animation: slideUp 0.4s ease-out;
            border-left: 4px solid {primary_color};
        }}
        
        @keyframes slideUp {{
            from {{ transform: translateY(15px); opacity: 0; }}
            to {{ transform: translateY(0); opacity: 1; }}
        }}
        
        /* Message metadata styling */
        .message-metadata {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
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
        <div class="sidebar-card">
            <div class="sidebar-card-header">
                <span class="feature-icon">✨</span> My Capabilities
            </div>
            <div class="features-grid">
                <div class="capability-tile">
                    <div class="capability-icon">🧠</div>
                    <div class="capability-text">Answer Questions</div>
                </div>
                <div class="capability-tile">
                    <div class="capability-icon">📝</div>
                    <div class="capability-text">Write Content</div>
                </div>
                <div class="capability-tile">
                    <div class="capability-icon">💡</div>
                    <div class="capability-text">Creative Ideas</div>
                </div>
                <div class="capability-tile">
                    <div class="capability-icon">📚</div>
                    <div class="capability-text">Summarize Text</div>
                </div>
                <div class="capability-tile">
                    <div class="capability-icon">🎮</div>
                    <div class="capability-text">Fun & Games</div>
                </div>
                <div class="capability-tile">
                    <div class="capability-icon">🧩</div>
                    <div class="capability-text">Solve Problems</div>
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

import streamlit as st
from pymongo import MongoClient
from datetime import datetime
import os

# MongoDB Connection and Initialization
def initialize_mongodb():
    """
    Establish connection to MongoDB database
    """
    try:
        # Prioritize Streamlit secrets, fallback to environment variables
        # Ensure you have set up MongoDB connection string in Streamlit secrets or environment
        connection_string = (
            st.secrets.get("mongodb", {}).get("connection_string") or 
            os.environ.get("MONGODB_CONNECTION_STRING")
        )
        
        # Database and collection names
        db_name = st.secrets.get("mongodb", {}).get("database", "ai_assistant")
        conversations_collection = st.secrets.get("mongodb", {}).get("conversations_collection", "conversations")
        users_collection = st.secrets.get("mongodb", {}).get("users_collection", "users")
        
        if not connection_string:
            st.error("MongoDB connection string not found. Please configure in Streamlit secrets.")
            return None
        
        # Create MongoDB client
        client = MongoClient(connection_string)
        db = client[db_name]
        
        # Ensure collections exist and create indexes
        conversations_coll = db[conversations_collection]
        users_coll = db[users_collection]
        
        # Create indexes for efficient querying
        conversations_coll.create_index([("timestamp", -1)])
        users_coll.create_index("username", unique=True)
        
        return {
            "client": client,
            "db": db,
            "conversations": conversations_coll,
            "users": users_coll
        }
    
    except Exception as e:
        st.error(f"MongoDB initialization error: {e}")
        return None

# Function to save conversation to MongoDB
def save_conversation(user_message, assistant_response, user_id=None):
    """
    Save a conversation turn to MongoDB
    
    :param user_message: User's input message
    :param assistant_response: AI's response
    :param user_id: Optional user identifier
    """
    try:
        mongo_conn = initialize_mongodb()
        if mongo_conn:
            conversation_doc = {
                "user_message": user_message,
                "assistant_response": assistant_response,
                "timestamp": datetime.utcnow(),
                "user_id": user_id  # Optional user tracking
            }
            
            # Insert conversation document
            mongo_conn["conversations"].insert_one(conversation_doc)
            
            # Optionally update user document
            if user_id:
                mongo_conn["users"].update_one(
                    {"_id": user_id},
                    {
                        "$inc": {"total_conversations": 1},
                        "$set": {"last_interaction": datetime.utcnow()}
                    },
                    upsert=True
                )
    
    except Exception as e:
        st.error(f"Error saving conversation: {e}")

# Function to retrieve conversation history
def get_conversation_history(limit=50, user_id=None):
    """
    Retrieve recent conversation history from MongoDB
    
    :param limit: Number of recent conversations to retrieve
    :param user_id: Optional user identifier to filter conversations
    :return: List of conversation documents
    """
    try:
        mongo_conn = initialize_mongodb()
        if mongo_conn:
            query = {"user_id": user_id} if user_id else {}
            
            # Retrieve conversations, sorted by most recent first
            history = list(
                mongo_conn["conversations"]
                .find(query)
                .sort("timestamp", -1)
                .limit(limit)
            )
            
            return history
    
    except Exception as e:
        st.error(f"Error retrieving conversation history: {e}")
        return []

# Function to create or get user
def get_or_create_user(username):
    """
    Create a new user or retrieve existing user document
    
    :param username: Username to create/retrieve
    :return: User document
    """
    try:
        mongo_conn = initialize_mongodb()
        if mongo_conn:
            # Try to find existing user
            user = mongo_conn["users"].find_one({"username": username})
            
            # If user doesn't exist, create new user
            if not user:
                user_doc = {
                    "username": username,
                    "total_conversations": 0,
                    "created_at": datetime.utcnow(),
                    "last_interaction": datetime.utcnow()
                }
                result = mongo_conn["users"].insert_one(user_doc)
                user = mongo_conn["users"].find_one({"_id": result.inserted_id})
            
            return user
    
    except Exception as e:
        st.error(f"Error managing user: {e}")
        return None

# Enhanced chat QA function with MongoDB integration
def enhanced_chat_qa(prompt, username=None):
    """
    Enhanced chat QA function that saves conversation to MongoDB
    
    :param prompt: User's input message
    :param username: Optional username for tracking
    :return: AI's response
    """
    # Perform existing chat QA logic (Groq API call)
    response = chat_qa(prompt)
    
    # Get or create user if username provided
    user = get_or_create_user(username) if username else None
    
    # Save conversation to MongoDB
    save_conversation(
        user_message=prompt, 
        assistant_response=response, 
        user_id=user["_id"] if user else None
    )
    
    return response

# Modify main Streamlit app setup
if "messages" not in st.session_state:
    # Try to load recent conversation history from MongoDB
    mongo_conn = initialize_mongodb()
    if mongo_conn:
        db_history = get_conversation_history(limit=10)
        
        # Convert MongoDB history to session state messages format
        st.session_state.messages = [
            {
                "role": "user", 
                "content": entry.get("user_message", ""), 
                "timestamp": entry["timestamp"].strftime("%I:%M %p")
            },
            {
                "role": "assistant", 
                "content": entry.get("assistant_response", ""), 
                "timestamp": entry["timestamp"].strftime("%I:%M %p")
            }
        ] for entry in db_history
    else:
        st.session_state.messages = []

# Modify chat interaction to use enhanced_chat_qa
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
    
    # Get Response from enhanced chatbot function
    # Optionally pass a username for user tracking
    response = enhanced_chat_qa(prompt, username="default_user")
    
    # Display assistant message
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response,
        "timestamp": datetime.now().strftime("%I:%M %p")
    })
    st.session_state.message_count += 1
    
    # Force a rerun to display the updated conversation
    st.rerun()

# Sidebar function to view conversation history
def show_conversation_history():
    """
    Display a sidebar option to view conversation history
    """
    if st.sidebar.button("View Conversation History"):
        history = get_conversation_history(limit=20)
        st.sidebar.markdown("### Conversation History")
        for idx, entry in enumerate(history, 1):
            st.sidebar.markdown(f"**Conversation {idx}** *({entry['timestamp'].strftime('%Y-%m-%d %H:%M')})*")
            st.sidebar.markdown(f"👤 User: {entry.get('user_message', 'N/A')}")
            st.sidebar.markdown(f"🤖 AI: {entry.get('assistant_response', 'N/A')}")
            st.sidebar.markdown("---")

# Call the history viewing function in sidebar setup
show_conversation_history()