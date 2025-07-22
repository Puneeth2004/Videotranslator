import os
import tempfile
import nltk
import whisper
import ffmpeg
from googletrans import Translator
from gtts import gTTS
import pygame
import time

# Download required NLTK data
nltk.download('punkt')

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

def transcribe_audio(audio_path):
    """Transcribes audio using Whisper"""
    result = model.transcribe(audio_path)
    return result["text"]

def translate_to_telugu(text):
    """Translates English text to Telugu using Google Translate"""
    translator = Translator()
    translated = translator.translate(text, dest="te")
    return translated.text

def speak_text(text, lang='ta'):
    """Converts Telugu text to speech and plays it"""
    tts = gTTS(text=text, lang=lang)
    temp_mp3 = "temp_audio.mp3"
    tts.save(temp_mp3)

    pygame.mixer.init()
    pygame.mixer.music.load(temp_mp3)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.5)

    pygame.mixer.music.unload()
    os.remove(temp_mp3)
