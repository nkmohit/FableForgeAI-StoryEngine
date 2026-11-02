import os

import streamlit as st
from dotenv import load_dotenv

from gemini_utility import check_api_key, get_available_models

load_dotenv()

# GEMINI_API_KEY is the documented name; GOOGLE_API_KEY still works.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

st.set_page_config(
    page_title="FableForge",
    page_icon=":material/menu_book:",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/your-repo",
        "Report a bug": "https://github.com/your-repo/issues",
        "About": "FableForge. Chat, stories, comic video, and a writing assistant.",
    },
)

if not GEMINI_API_KEY:
    st.error("Set GEMINI_API_KEY or GOOGLE_API_KEY in the .env file.")
    st.stop()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "api_status" not in st.session_state:
    st.session_state.api_status = check_api_key()

with st.sidebar:
    if st.session_state.api_status:
        st.caption("Gemini API connected")
    else:
        st.caption("Gemini API unavailable")

    st.divider()

    available_models = get_available_models()
    st.selectbox(
        "Model",
        available_models[:5],
        key="selected_model",
        help="Used for every Gemini request.",
    )

    with st.expander("Generation"):
        st.slider(
            "Temperature",
            0.0,
            1.0,
            0.7,
            key="temperature",
            help="Lower is more predictable. Higher is more varied.",
        )
        st.slider(
            "Max tokens",
            100,
            2048,
            1000,
            key="max_tokens",
            help="Upper limit on the length of the reply.",
        )

pages = st.navigation(
    [
        st.Page("views/chat.py", title="Chat", default=True, url_path="chat"),
        st.Page("views/stories.py", title="Stories", url_path="stories"),
        st.Page("views/comic_video.py", title="Comic video", url_path="comic-video"),
        st.Page("views/assistant.py", title="Assistant", url_path="assistant"),
    ],
    expanded=True,
)
pages.run()
