import streamlit as st
import requests
import uuid

# Config
RASA_URL = "http://localhost:5005/webhooks/rest/webhook"

st.set_page_config(
    page_title="RetailBot", 
    page_icon="🤖", 
    layout="wide"
)

# Title
st.title("🤖 RetailBot")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "sender_id" not in st.session_state:
    st.session_state.sender_id = str(uuid.uuid4())

# Chat styling
st.markdown("""
<style>
    .chat-container {
        max-height: 60vh;
        overflow-y: auto;
        padding: 10px;
        margin-bottom: 80px;
    }
    .user-message {
        background-color: #DCF8C6;
        padding: 8px 12px;
        border-radius: 8px;
        margin: 6px 0;
        max-width: 80%;
        margin-left: auto;
    }
    .bot-message {
        background-color: #FFFFFF;
        padding: 8px 12px;
        border-radius: 8px;
        margin: 6px 0;
        max-width: 80%;
        margin-right: auto;
        border: 1px solid #eee;
    }
    .input-container {
        position: fixed;
        bottom: 20px;
        width: calc(100% - 40px);
        background: white;
        padding: 10px;
        border-radius: 8px;
        box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
def send_to_rasa(message):
    payload = {
        "sender": st.session_state.sender_id,
        "message": message
    }
    try:
        response = requests.post(RASA_URL, json=payload, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return [{"text": f"⚠️ Error: {str(e)}"}]

# Display chat messages
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(
                f'<div class="user-message">{message["content"]}</div>', 
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="bot-message">{message["content"]}</div>', 
                unsafe_allow_html=True
            )

# Input form
with st.form("chat_input", clear_on_submit=True):
    cols = st.columns([10, 1])
    with cols[0]:
        user_input = st.text_input(
            "Type your message", 
            "", 
            key="input",
            label_visibility="collapsed"
        )
    with cols[1]:
        submitted = st.form_submit_button("Send")

if submitted and user_input:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get bot response
    with st.spinner("Thinking..."):
        responses = send_to_rasa(user_input)
    
    # Add bot responses to chat
    for response in responses:
        if "text" in response:
            st.session_state.messages.append({"role": "bot", "content": response["text"]})
    
    # Rerun to update chat display
    st.rerun()