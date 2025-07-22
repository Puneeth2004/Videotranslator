import streamlit as st
from utils import extract_audio, transcribe_audio, translate_to_telugu, speak_text

st.set_page_config(page_title="🎥 Video to Telugu Translator", layout="centered")

st.title("🎥 English Video to Telugu Translator")

video_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi"])

if video_file:
    with open("temp_video.mp4", "wb") as f:
        f.write(video_file.read())

    st.info("Extracting audio...")
    audio_path = extract_audio("temp_video.mp4")

    st.info("Transcribing audio...")
    english_text = transcribe_audio(audio_path)
    st.success("Transcription Complete!")

    st.subheader("English Transcript")
    st.write(english_text)

    st.info("Translating transcript to Telugu...")
    telugu_translation = translate_to_telugu(english_text)
    st.subheader("Telugu Translation")
    st.write(telugu_translation)

    # Speak aloud switch
    speak_aloud = st.toggle("🔊 Speak Aloud Telugu Translation")

    if speak_aloud:
        st.info("Speaking the translated text...")
        speak_text(telugu_translation)
