import streamlit as st
from utils2 import (
    extract_audio,
    transcribe_with_timestamps,
    translate_text,
    speak_text,
    download_youtube_video,
)
import time

st.set_page_config(page_title="Video Translator", layout="wide")

st.sidebar.header("Controls")
video_file = st.sidebar.file_uploader("Upload Video", type=["mp4", "mov", "avi"])
youtube_url = st.sidebar.text_input("Or paste YouTube link")

language_display = {
    "Telugu": "te",
    "Hindi": "hi",
    "Tamil": "ta",
    "Kannada": "kn"
}
selected_lang = st.sidebar.selectbox("🌐 Translation Language", list(language_display.keys()))
tts_lang_code = language_display[selected_lang]

if "play_audio" not in st.session_state:
    st.session_state.play_audio = False
if "proceed" not in st.session_state:
    st.session_state.proceed = False

def toggle_audio():
    st.session_state.play_audio = not st.session_state.play_audio

def reset_app():
    st.session_state.play_audio = False
    st.session_state.proceed = False
    st.session_state.youtube_url = ""
    st.rerun()

st.sidebar.button("🔊 Toggle Audio Playback", on_click=toggle_audio)
st.sidebar.button("▶️ Proceed", on_click=lambda: st.session_state.update({"proceed": True}))
st.sidebar.button("🔄 Reset", on_click=reset_app)

st.title("🎥 English Video to Multilingual Translator")

video_path = None
if st.session_state.proceed:
    if video_file is not None:
        with open("uploaded_video.mp4", "wb") as f:
            f.write(video_file.read())
        video_path = "uploaded_video.mp4"
    elif youtube_url:
        with st.spinner("📥 Downloading audio from YouTube..."):
            video_path = download_youtube_video(youtube_url)
        st.success("YouTube audio downloaded!")

    if video_path:
        with st.spinner("🎧 Extracting audio..."):
            audio_path = extract_audio(video_path)
        st.success("Audio extracted!")

        with st.spinner("📝 Transcribing..."):
            transcript_segments = transcribe_with_timestamps(audio_path)
        st.success("✅ Transcription complete")

        st.subheader("🗒️ Transcript with Timestamps")
        for seg in transcript_segments:
            start_time = time.strftime("%H:%M:%S", time.gmtime(seg['start']))
            end_time = time.strftime("%H:%M:%S", time.gmtime(seg['end']))
            st.markdown(f"**[{start_time} - {end_time}]**: {seg['text']}")

        full_english_text = " ".join([seg['text'] for seg in transcript_segments])

        with st.spinner(f"🌐 Translating to {selected_lang}..."):
            translated_text = translate_text(full_english_text, target_lang=tts_lang_code)
        st.success(f"Translation to {selected_lang} complete!")

        st.subheader(f"🈯 Translation in {selected_lang}")
        st.write(translated_text)

        st.subheader("🔊 Translated Audio Playback")
        if st.session_state.play_audio:
            st.info("🔊 Playing translated audio...")
            speak_text(translated_text, lang=tts_lang_code, stop_flag=lambda: st.session_state.play_audio)
        else:
            st.info("🔇 Audio is stopped.")
    else:
        st.warning("Please upload a video or provide a YouTube link.")
else:
    st.info("Click ▶️ Proceed to start processing.")
