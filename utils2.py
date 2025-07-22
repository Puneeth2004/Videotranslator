import os
import tempfile
import whisper
import ffmpeg
from deep_translator import GoogleTranslator
from gtts import gTTS
import pygame
import time
import subprocess

# Load Whisper model
model = whisper.load_model("tiny")


def extract_audio(video_path):
    """Extracts audio from video and saves as temporary .wav file"""
    temp_audio_fd, temp_audio_path = tempfile.mkstemp(suffix=".wav")
    os.close(temp_audio_fd)

    (
        ffmpeg
        .input(video_path)
        .output(temp_audio_path, format='wav', acodec='pcm_s16le', ac=1, ar='16k')
        .run(overwrite_output=True)
    )
    return temp_audio_path


def transcribe_with_timestamps(audio_path):
    """Transcribes audio and returns segments with timestamps"""
    result = model.transcribe(audio_path)
    segments = result['segments']
    return [{"start": seg["start"], "end": seg["end"], "text": seg["text"].strip()} for seg in segments]


def translate_text(text, target_lang="te"):
    """Translates text using Deep Translator"""
    return GoogleTranslator(source='auto', target=target_lang).translate(text)


def speak_text(text, lang='te', stop_flag=None):
    """Converts text to speech and plays it with toggleable stop"""
    temp_mp3 = "temp_audio.mp3"
    tts = gTTS(text=text, lang=lang)
    tts.save(temp_mp3)

    pygame.mixer.init()
    pygame.mixer.music.load(temp_mp3)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        if stop_flag is not None and not stop_flag():
            pygame.mixer.music.stop()
            break
        time.sleep(0.3)

    pygame.mixer.quit()
    try:
        os.remove(temp_mp3)
    except PermissionError:
        pass


def download_youtube_video(url):
    """
    Downloads a YouTube video using yt-dlp and returns the path to the .mp4 file
    """
    try:
        temp_fd, temp_path = tempfile.mkstemp(suffix=".mp4")
        os.close(temp_fd)
        os.remove(temp_path)  # yt-dlp will create it with proper content

        subprocess.run([
            "yt-dlp",
            "-f", "best[ext=mp4]",
            "-o", temp_path,
            url
        ], check=True)

        return temp_path

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to fetch video via yt-dlp: {str(e)}")
def reset_app():
    st.session_state.play_audio = False
    st.session_state.proceed = False
    st.session_state.youtube_url = ""
    st.rerun()  # updated!
