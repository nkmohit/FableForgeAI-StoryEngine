import streamlit as st

from app_ui import gemini_call_kwargs
from gemini_utility import gemini_pro_response

st.title("Assistant")
st.caption("Rewrite, check, summarize, or translate text you paste in.")

assistant_type = st.selectbox(
    "Assistant",
    ["Writing", "Research", "Ideas", "Creative", "Tutor"],
)

if assistant_type == "Writing":
    task = st.selectbox(
        "Task",
        ["Improve Text", "Grammar Check", "Summarize", "Translate", "Change Tone", "Expand Ideas"],
    )
    user_text = st.text_area("Text", height=200)

    if task == "Change Tone":
        tone = st.selectbox("Tone", ["Professional", "Casual", "Friendly", "Formal", "Persuasive"])
    elif task == "Translate":
        language = st.selectbox(
            "Language",
            ["Spanish", "French", "German", "Italian", "Japanese", "Chinese"],
        )

    if st.button(task, type="primary"):
        if user_text:
            if task == "Change Tone":
                prompt = f"Rewrite this text in a {tone.lower()} tone: {user_text}"
            elif task == "Translate":
                prompt = f"Translate this text to {language}: {user_text}"
            else:
                prompt = f"{task} this text: {user_text}"

            result = gemini_pro_response(prompt, **gemini_call_kwargs())
            st.subheader("Result")
            st.write(result)
else:
    st.caption("This assistant is not available yet.")
