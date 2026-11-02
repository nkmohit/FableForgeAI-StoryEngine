import streamlit as st

from app_ui import gemini_call_kwargs
from gemini_utility import (
    build_generation_config,
    gemini_stream_response,
    load_gemini_pro_model,
)


def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    return user_role


selected_model = st.session_state["selected_model"]
temperature = st.session_state["temperature"]
max_tokens = st.session_state["max_tokens"]

model = load_gemini_pro_model(selected_model)

# Recreate the chat when the selected model changes so the dropdown takes effect.
if (
    "chat_session" not in st.session_state
    or st.session_state.get("chat_model") != selected_model
):
    st.session_state.chat_session = model.start_chat(history=[])
    st.session_state.chat_model = selected_model

st.title("Chat")
st.caption("Messages stay in this session. Stream shows the reply as it arrives.")

clear_col, save_col, stats_col, voice_col, stream_col = st.columns(
    [1, 1, 1, 1, 1.4], gap="small"
)
with clear_col:
    clear_chat = st.button("Clear chat")
with save_col:
    save_chat = st.button("Save chat")
with stats_col:
    show_stats = st.button("Chat stats")
with voice_col:
    voice_input = st.button("Voice input")
with stream_col:
    stream_mode = st.toggle("Stream", help="Show the reply as it arrives.")

if clear_chat:
    st.session_state.chat_session = model.start_chat(history=[])
    st.rerun()

if save_chat:
    st.download_button(
        "Download chat",
        data=str(st.session_state.chat_session.history),
        file_name="chat_history.txt",
        mime="text/plain",
    )

if show_stats:
    st.caption(f"{len(st.session_state.chat_session.history)} messages in this chat.")

if voice_input:
    st.caption("Voice input is not available yet.")

chat_container = st.container(height=400)

with chat_container:
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

user_prompt = st.chat_input("Message")

if user_prompt:
    with chat_container:
        with st.chat_message("user"):
            st.markdown(user_prompt)

    with chat_container:
        with st.chat_message("assistant"):
            if stream_mode:
                response_placeholder = st.empty()
                response_text = ""

                try:
                    response = gemini_stream_response(user_prompt, **gemini_call_kwargs())
                    for chunk in response:
                        if hasattr(chunk, "text"):
                            response_text += chunk.text
                            response_placeholder.markdown(response_text + "▌")
                    response_placeholder.markdown(response_text)

                    # Update session manually for streaming.
                    st.session_state.chat_session.history.append(
                        type("Message", (), {"role": "user", "parts": [type("Part", (), {"text": user_prompt})]})()
                    )
                    st.session_state.chat_session.history.append(
                        type("Message", (), {"role": "model", "parts": [type("Part", (), {"text": response_text})]})()
                    )
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                try:
                    gemini_response = st.session_state.chat_session.send_message(
                        user_prompt,
                        generation_config=build_generation_config(temperature, max_tokens),
                    )
                    st.markdown(gemini_response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
