import time

import streamlit as st
from PIL import Image

from app_ui import gemini_call_kwargs, text2speech
from gemini_utility import gemini_pro_response, gemini_pro_vision_response

st.title("Stories")
st.caption("Write from an image, a prompt, or a short brief.")

image_tab, text_tab, writing_tab = st.tabs(["Image and text", "Text", "Creative writing"])

with image_tab:
    st.caption("The story uses the image and the notes you add.")
    image_col, details_col = st.columns(2, gap="large")

    with image_col:
        uploaded_image = st.file_uploader(
            "Image",
            type=["jpg", "jpeg", "png", "webp"],
            help="JPG, JPEG, PNG, or WEBP.",
        )
        if uploaded_image:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded image", use_container_width=True)

    with details_col:
        user_text = st.text_area(
            "Theme or details",
            placeholder="A quiet street after rain.",
            height=100,
            key="image_story_text",
        )
        story_length = st.selectbox(
            "Length",
            ["Short (5-10 lines)", "Medium (10-20 lines)", "Long (20-30 lines)"],
            key="image_story_length",
        )
        story_genre = st.selectbox(
            "Genre",
            ["Adventure", "Mystery", "Romance", "Horror", "Comedy", "Sci-Fi", "Fantasy"],
            key="image_story_genre",
        )
        include_moral = st.checkbox("Include a moral", value=True)
        generate_audio = st.checkbox("Generate audio", value=True)
        generate_image_story = st.button(
            "Generate story", type="primary", key="generate_image_story"
        )

    if generate_image_story:
        if uploaded_image is not None and user_text.strip():
            with st.spinner("Writing the story..."):
                length_map = {
                    "Short (5-10 lines)": "5-10 lines",
                    "Medium (10-20 lines)": "10-20 lines",
                    "Long (20-30 lines)": "20-30 lines",
                }

                prompt = f"""
                    Generate a {story_genre.lower()} story based on this image with the following requirements:
                    - Theme/Details: {user_text}
                    - Length: {length_map[story_length]}
                    - Genre: {story_genre}
                    - Include moral lesson: {include_moral}

                    Make the story engaging, creative, and well-structured.
                    """

                story = gemini_pro_vision_response(prompt, image, **gemini_call_kwargs())

                result_image, result_text = st.columns(2, gap="large")
                with result_image:
                    st.image(image, caption="Story inspiration", use_container_width=True)
                with result_text:
                    st.subheader("Story")
                    st.write(story)

                    if generate_audio and story:
                        with st.spinner("Generating audio..."):
                            audio_bytes = text2speech(story)
                            if audio_bytes:
                                st.audio(audio_bytes, format="audio/wav")

                    st.download_button(
                        "Download story",
                        story,
                        file_name=f"story_{int(time.time())}.txt",
                        mime="text/plain",
                        key="download_image_story",
                    )

with text_tab:
    st.caption("Describe the idea. Length, tone, and audience are sent with it.")
    prompt_col, settings_col = st.columns([2, 1], gap="large")

    with prompt_col:
        text_story = st.text_area(
            "Story idea",
            placeholder="Characters, setting, or plot.",
            height=150,
            key="text_story_idea",
        )
        generate_text_story = st.button(
            "Generate story", type="primary", key="generate_text_story"
        )

    with settings_col:
        st.subheader("Settings")
        text_length = st.radio("Length", ["Short", "Medium", "Long"], key="text_story_length")
        text_tone = st.selectbox(
            "Tone",
            ["Cheerful", "Dark", "Mysterious", "Humorous", "Dramatic"],
            key="text_story_tone",
        )
        text_audience = st.selectbox(
            "Audience",
            ["Children", "Teenagers", "Adults", "All Ages"],
            key="text_story_audience",
        )

    if generate_text_story:
        if text_story.strip():
            with st.spinner("Writing the story..."):
                prompt = f"""
                    Create a {text_length.lower()} {text_tone.lower()} story suitable for {text_audience.lower()} 
                    based on: {text_story}

                    Make it engaging and include a meaningful conclusion.
                    """

                story = gemini_pro_response(prompt, **gemini_call_kwargs())

                st.subheader("Story")
                st.write(story)

                if st.checkbox("Generate audio", key="text_story_audio"):
                    with st.spinner("Generating audio..."):
                        audio_bytes = text2speech(story)
                        if audio_bytes:
                            st.audio(audio_bytes, format="audio/wav")

with writing_tab:
    writing_type = st.selectbox(
        "Type",
        ["Poem", "Song Lyrics", "Short Story", "Character Description", "World Building", "Dialogue"],
    )

    if writing_type == "Poem":
        style_col, mood_col = st.columns(2, gap="large")
        with style_col:
            poem_style = st.selectbox("Style", ["Free Verse", "Haiku", "Sonnet", "Limerick"])
            theme = st.text_input("Theme", placeholder="Love, nature, adventure")
        with mood_col:
            mood = st.selectbox("Mood", ["Happy", "Sad", "Peaceful", "Energetic"])
            length = st.selectbox("Length", ["Short", "Medium", "Long"], key="poem_length")

        if st.button("Generate poem", type="primary"):
            prompt = f"Write a {poem_style.lower()} poem about {theme} with a {mood.lower()} mood. Length: {length.lower()}"
            result = gemini_pro_response(prompt, **gemini_call_kwargs())
            st.write(result)
    else:
        st.caption("Only poems can be generated here.")
