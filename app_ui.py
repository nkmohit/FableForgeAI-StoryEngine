"""Shared UI helpers. Page scripts read generation settings from session state."""

import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")


def gemini_call_kwargs():
    """Sidebar settings that every Gemini request should honor."""
    return {
        "temperature": st.session_state["temperature"],
        "max_output_tokens": st.session_state["max_tokens"],
        "model_name": st.session_state["selected_model"],
    }


def text2speech(text):
    """Convert text to speech using the Hugging Face inference API."""
    if not HUGGINGFACE_API_KEY:
        st.warning("Hugging Face token not found. Audio generation is off.")
        return None

    api_url = "https://api-inference.huggingface.co/models/facebook/mms-tts-eng"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {"inputs": text}

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.content
        st.error(f"Audio generation failed. Status: {response.status_code}")
        return None
    except Exception as e:
        st.error(f"Audio generation error: {e}")
        return None
