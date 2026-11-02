import time

import streamlit as st
from gradio_client import Client

from app_ui import gemini_call_kwargs
from gemini_utility import gemini_pro_response

# client.predict sends only the script, so style, duration, character, and audio
# controls are not shown.
st.title("Comic video")
st.caption(
    "Sends the script to the Hugging Face Space ADOPLE/Video-Generator-AI and plays the video that Space returns."
)

script_col, preview_col = st.columns([2, 1], gap="large")

with script_col:
    st.subheader("Script")
    user_prompt = st.text_area(
        "Script",
        placeholder="Write the story or script for the video.",
        height=200,
        label_visibility="collapsed",
    )
    generate_video = st.button("Generate video", type="primary")

with preview_col:
    st.subheader("Preview")
    preview_story = st.button("Preview")

if preview_story and user_prompt:
    enhanced_prompt = f"Enhance this story for comic video: {user_prompt}"
    enhanced_story = gemini_pro_response(enhanced_prompt, **gemini_call_kwargs())
    st.subheader("Revised script")
    st.write(enhanced_story)

if generate_video:
    if user_prompt.strip():
        with st.spinner("Generating the video. This can take a few minutes."):
            try:
                client = Client("ADOPLE/Video-Generator-AI")
                result = client.predict(
                    user_prompt,
                    api_name="/generate_video",
                )

                if result and "video" in result:
                    video_data = result["video"]
                    st.success("Video ready.")
                    st.video(video_data)
                    st.download_button(
                        "Download video",
                        data=video_data,
                        file_name=f"comic_video_{int(time.time())}.mp4",
                        mime="video/mp4",
                    )
                else:
                    st.error("Video generation failed. Try again.")
            except Exception as e:
                st.error(f"Error generating video: {e}")
                st.info("Try a shorter script, or check the connection to the video service.")
