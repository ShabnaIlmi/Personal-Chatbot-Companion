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
    page_title="Enterprise Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define professional color scheme
primary_color = "#2C3E50"    # Dark blue/slate
secondary_color = "#3498DB"  # Blue
accent_color = "#ECF0F1"     # Light gray
text_color = "#2C3E50"       # Dark blue/slate
light_bg = "#FFFFFF"         # White
message_bg_user = "#F8F9FA"  # Very light gray
message_bg_assistant = "#EBF5FB"  # Very light blue

# Inject custom CSS for professional UI
st.markdown(
    f"""
    <style>
        /* Overall app styling */
        .stApp {{
            background-color: #F5F7F9;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }}
        
        /* Scrollbar styling */
        ::-webkit-scrollbar {{
            width: 6px;
            height: 6px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: #F1F1F1;
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: #CBD5E0;
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: #A0AEC0;
        }}
        
        /* Header Styling */
        .header-container {{
            padding: 20px 0 10px 0;
            border-bottom: 1px solid #E2E8F0;
            margin-bottom: 20px;
            background-color: {light_bg};
        }}
        
        .header-title {{
            font-size: 1.5rem;
            font-weight: 600;
            color: {primary_color};
            margin: 0;
        }}
        
        .header-subtitle {{
            font-size: 0.9rem;
            color: #718096;
            margin-top: 5px;
        }}
        
        /* Stats bar styling */
        .stats-container {{
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
            padding: 10px 0;
            border-bottom: 1px solid #E2E8F0;
        }}
        
        .stat-item {{
            display: flex;
            align-items: center;
            font-size: 0.8rem;
            color: #718096;
        }}
        
        .stat-label {{
            margin-right: 5px;
        }}
        
        .stat-value {{
            font-weight: 600;
            color: {primary_color};
        }}
        
        /* Chat Container Styling */
        .chat-container {{
            background-color: {light_bg};
            padding: 20px;
            border-radius: 6px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            margin-bottom: 20px;
            height: 60vh;
            overflow-y: auto;
            border: 1px solid #E2E8F0;
        }}
        
        /* User's message styling */
        .user-message {{
            background-color: {message_bg_user};
            border-radius: 6px;
            padding: 12px 16px;
            margin-bottom: 12px;
            font-size: 0.95rem;
            color: {text_color};
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
            align-self: flex-end;
            max-width: 85%;
            word-wrap: break-word;
            position: relative;
            margin-left: auto;
            border-left: 3px solid {secondary_color};
        }}
        
        /* Assistant's message styling */
        .assistant-message {{
            background-color: {message_bg_assistant};
            border-radius: 6px;
            padding: 12px 16px;
            margin-bottom: 12px;
            font-size: 0.95rem;
            color: {text_color};
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
            align-self: flex-start;
            max-width: 85%;
            word-wrap: break-word;
            position: relative;
            margin-right: auto;
            border-left: 3px solid {primary_color};
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
            font-size: 0.8rem;
        }}
        
        .user-sender {{
            color: {secondary_color};
        }}
        
        .assistant-sender {{
            color: {primary_color};
        }}
        
        /* Timestamp styling */
        .timestamp {{
            font-size: 0.7rem;
            color: #A0AEC0;
        }}
        
        /* Typing indicator */
        .typing-indicator {{
            background-color: {message_bg_assistant};
            border-radius: 6px;
            padding: 12px 16px;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            border-left: 3px solid {primary_color};
            width: fit-content;
        }}
        
        .typing-indicator .dot {{
            height: 8px;
            width: 8px;
            margin: 0 2px;
            background-color: #A0AEC0;
            border-radius: 50%;
            opacity: 0.6;
        }}
        
        .typing-indicator .dot:nth-child(1) {{
            animation: pulse 1.2s infinite 0.1s;
        }}
        
        .typing-indicator .dot:nth-child(2) {{
            animation: pulse 1.2s infinite 0.3s;
        }}
        
        .typing-indicator .dot:nth-child(3) {{
            animation: pulse 1.2s infinite 0.5s;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); opacity: 0.6; }}
            50% {{ transform: scale(1.1); opacity: 0.9; }}
        }}
        
        /* Input area styling */
        .input-container {{
            background-color: {light_bg};
            padding: 15px;
            border-radius: 6px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            border: 1px solid #E2E8F0;
        }}
        
        /* Input Styling */
        .stTextInput input, .stChatInput input {{
            border-radius: 6px !important;
            border: 1px solid #E2E8F0 !important;
            padding: 10px 14px !important;
            font-size: 0.95rem !important;
            color: {text_color} !important;
            box-shadow: none !important;
        }}
        
        .stTextInput input:focus, .stChatInput input:focus {{
            border-color: {secondary_color} !important;
            box-shadow: 0 0 0 1px {secondary_color} !important;
        }}
        
        /* Footer styling */
        .footer {{
            text-align: center;
            font-size: 0.75rem;
            color: #A0AEC0;
            padding: 15px 0;
            border-top: 1px solid #E2E8F0;
            margin-top: 30px;
        }}
        
        /* Hide Streamlit branding */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        
        /* Code block styling */
        code {{
            border-radius: 4px;
            padding: 2px 5px;
            background-color: #F7FAFC;
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
            font-size: 0.85em;
            color: #2D3748;
        }}
        
        pre {{
            background-color: #F7FAFC;
            border-radius: 4px;
            padding: 10px;
            overflow-x: auto;
            border: 1px solid #EDF2F7;
        }}
        
        /* Sidebar styling */
        .css-1cypcdb, .css-163ttbj, .css-1ope8sv {{
            background-color: {light_bg};
        }}
        
        .css-pkbazv {{
            color: {primary_color} !important;
        }}
        
        /* Two-column layout */
        .main-content {{
            display: flex;
            gap: 20px;
        }}
        
        .chat-column {{
            flex: 3;
        }}
        
        .info-column {{
            flex: 1;
            min-width: 220px;
        }}
        
        .info-card {{
            background-color: {light_bg};
            border-radius: 6px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            border: 1px solid #E2E8F0;
        }}
        
        .info-card-header {{
            font-size: 0.9rem;
            font-weight: 600;
            color: {primary_color};
            margin-bottom: 10px;
            padding-bottom: 5px;
            border-bottom: 1px solid #E2E8F0;
        }}
        
        .info-list {{
            font-size: 0.8rem;
        }}
        
        .info-item {{
            display: flex;
            justify-content: space-between;
            padding: 5px 0;
            border-bottom: 1px solid #F7FAFC;
        }}
        
        .info-label {{
            color: #718096;
        }}
        
        .info-value {{
            font-weight: 500;
            color: {text_color};
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

# Get current time
current_time = datetime.now().strftime("%H:%M")
current_date = datetime.now().strftime("%b %d, %Y")

# Create a sidebar with additional controls
with st.sidebar:
    st.markdown('<div style="text-align: center; padding: 10px 0;"><h3>⚡ Enterprise AI</h3></div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Model selection (for future use)
    model = st.selectbox(
        "Model",
        ["Llama-3.3-70B", "Llama-3-70B", "Future models..."],
        index=0,
        disabled=True
    )
    
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.1,
        format="%.1f",
        disabled=True,
        help="Controls randomness of responses. Lower values are more deterministic."
    )
    
    st.markdown("---")
    
    # Example prompts
    st.markdown("### Quick Prompts")
    example_prompts = [
        "Summarize the latest quarterly report",
        "Draft an email to the team about the new project",
        "Help me troubleshoot an API issue",
        "Explain complex data in simple terms"
    ]
    
    for prompt in example_prompts:
        if st.button(prompt, key=f"btn_{prompt}"):
            # Add to existing messages and trigger chat
            st.session_state.prompt_value = prompt

    st.markdown("---")
    
    # About section
    st.markdown("### About")
    st.markdown(
        """
        Enterprise AI Assistant powered by Groq's Llama-3.3-70B model.
        
        For assistance, contact IT support.
        """
    )

# Create header section
st.markdown(
    f'''
    <div class="header-container">
        <h1 class="header-title">Enterprise AI Assistant</h1>
        <p class="header-subtitle">Powered by Llama 3.3 | {current_date}</p>
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
            <span class="stat-value">Llama-3.3-70B</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Messages:</span>
            <span class="stat-value">{st.session_state.message_count}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Temperature:</span>
            <span class="stat-value">0.5</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Status:</span>
            <span class="stat-value">Active</span>
        </div>
    </div>
    ''',
    unsafe_allow_html=True
)

# Main content area with two columns
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Left column - Chat interface
st.markdown('<div class="chat-column">', unsafe_allow_html=True)

# Welcome message when starting a new conversation
if not st.session_state.conversation_started:
    st.session_state.conversation_started = True
    welcome_message = {
        "role": "assistant", 
        "content": "Welcome to the Enterprise AI Assistant. How can I help you with your business needs today?",
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
                    <div class="timestamp">{timestamp}</div>
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
                    <div class="timestamp">{timestamp}</div>
                </div>
                {message["content"]}
            </div>
            ''', 
            unsafe_allow_html=True
        )

st.markdown('</div>', unsafe_allow_html=True)

# User Input Section
st.markdown('<div class="input-container">', unsafe_allow_html=True)
prompt = st.chat_input("Type your message here...", key="chat_input")
st.markdown('</div>', unsafe_allow_html=True)

# Close chat column
st.markdown('</div>', unsafe_allow_html=True)

# Right column - Additional info
st.markdown('<div class="info-column">', unsafe_allow_html=True)

# Model information card
st.markdown(
    '''
    <div class="info-card">
        <div class="info-card-header">Model Information</div>
        <div class="info-list">
            <div class="info-item">
                <span class="info-label">Model</span>
                <span class="info-value">Llama-3.3</span>
            </div>
            <div class="info-item">
                <span class="info-label">Version</span>
                <span class="info-value">70B</span>
            </div>
            <div class="info-item">
                <span class="info-label">Provider</span>
                <span class="info-value">Groq</span>
            </div>
            <div class="info-item">
                <span class="info-label">Max Tokens</span>
                <span class="info-value">4,096</span>
            </div>
        </div>
    </div>
    ''',
    unsafe_allow_html=True
)

# Session information card
st.markdown(
    f'''
    <div class="info-card">
        <div class="info-card-header">Session</div>
        <div class="info-list">
            <div class="info-item">
                <span class="info-label">Messages</span>
                <span class="info-value">{st.session_state.message_count}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Started</span>
                <span class="info-value">{current_time}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Date</span>
                <span class="info-value">{current_date}</span>
            </div>
        </div>
    </div>
    ''',
    unsafe_allow_html=True
)

# Capabilities information card
st.markdown(
    '''
    <div class="info-card">
        <div class="info-card-header">Capabilities</div>
        <div class="info-list">
            <div class="info-item">
                <span class="info-label">Data Analysis</span>
                <span class="info-value">✓</span>
            </div>
            <div class="info-item">
                <span class="info-label">Content Creation</span>
                <span class="info-value">✓</span>
            </div>
            <div class="info-item">
                <span class="info-label">Code Assistance</span>
                <span class="info-value">✓</span>
            </div>
            <div class="info-item">
                <span class="info-label">Problem Solving</span>
                <span class="info-value">✓</span>
            </div>
        </div>
    </div>
    ''',
    unsafe_allow_html=True
)

# Close info column
st.markdown('</div>', unsafe_allow_html=True)

# Close main content div
st.markdown('</div>', unsafe_allow_html=True)

# Check if there's a prompt value from sidebar buttons
if "prompt_value" in st.session_state and st.session_state.prompt_value:
    prompt = st.session_state.prompt_value
    # Clear the value after using it
    st.session_state.prompt_value = None

if prompt:
    # Get current time
    current_time = datetime.now().strftime("%H:%M")
    
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
        "timestamp": datetime.now().strftime("%H:%M")
    })
    st.session_state.message_count += 1
    
    # Force a rerun to display the updated conversation
    st.rerun()

# Footer
st.markdown(
    '''
    <div class="footer">
        Enterprise AI Assistant | Powered by Groq | © 2025 Your Company Name
    </div>
    ''', 
    unsafe_allow_html=True
)