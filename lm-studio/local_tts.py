import os
import tempfile
import shutil
from gtts import gTTS

SUPPORTED_LANGS = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "ja": "Japanese",
    "ko": "Korean",
    "zh": "Chinese",
    "el": "Greek",
}

def play_audio(filename, player=None):
    if player == "mpg123" or (player is None and shutil.which("mpg123")):
        os.system(f"mpg123 -q {filename}")
    elif player == "ffplay" or (player is None and shutil.which("ffplay")):
        os.system(f"ffplay -nodisp -autoexit -loglevel quiet {filename}")
    else:
        print("No supported audio player found.")

def text_to_speech(text, lang="en", player=None):
    if lang not in SUPPORTED_LANGS:
        print(f"Language '{lang}' not supported. Falling back to English.")
        lang = "en"
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        filename = tmp.name
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)
    play_audio(filename, player=player)
    os.remove(filename)

def choose_language(current_lang="en"):
    print("Available languages:")
    for code, name in SUPPORTED_LANGS.items():
        print(f"{code}: {name}")
    lang = input(f"Select language code (current '{current_lang}'): ").strip().lower()
    if lang not in SUPPORTED_LANGS:
        print("Invalid choice. Keeping current language.")
        lang = current_lang
    print(f"Language set to: {SUPPORTED_LANGS[lang]}")
    return lang

def speak_gpt_response(text, lang="en", player=None):
    text_to_speech(text, lang=lang, player=player)
