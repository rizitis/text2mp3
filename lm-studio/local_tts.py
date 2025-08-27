import os
import shutil
import asyncio
from edge_tts import Communicate

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

async def _speak_edge_tts(text, voice="en-US-AriaNeural", filename="tts_output.mp3"):
    communicate = Communicate(text, voice)
    await communicate.save(filename)

def text_to_speech(text, lang="en", player=None):
    if lang not in SUPPORTED_LANGS:
        print(f"Language '{lang}' not supported. Falling back to English.")
        lang = "en"

    # Map language codes to Microsoft voices (you can adjust these)
    lang_voice_map = {
        "en": "en-US-AriaNeural",
        "es": "es-ES-ElviraNeural",
        "fr": "fr-FR-DeniseNeural",
        "de": "de-DE-KatjaNeural",
        "it": "it-IT-ElsaNeural",
        "pt": "pt-PT-HeloisaNeural",
        "ja": "ja-JP-NanamiNeural",
        "ko": "ko-KR-SunHiNeural",
        "zh": "zh-CN-XiaoxiaoNeural",
        "el": "el-GR-AthinaNeural",
    }

    voice = lang_voice_map.get(lang, "en-US-AriaNeural")
    filename = "tts_output.mp3"
    asyncio.run(_speak_edge_tts(text, voice=voice, filename=filename))
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
