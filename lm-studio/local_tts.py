import os
import platform
from kokoro import KPipeline
import soundfile as sf

SUPPORTED_LANGS = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
}

# Initialize Kokoro pipelines for supported languages
PIPELINES = {
    "en": KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M"),
    "es": KPipeline(lang_code="e", repo_id="hexgrad/Kokoro-82M"),
    "fr": KPipeline(lang_code="f", repo_id="hexgrad/Kokoro-82M"),
    "de": KPipeline(lang_code="b", repo_id="hexgrad/Kokoro-82M"),
    "it": KPipeline(lang_code="i", repo_id="hexgrad/Kokoro-82M"),
    "pt": KPipeline(lang_code="p", repo_id="hexgrad/Kokoro-82M"),
}

def play_audio(filename):
    """Play audio file cross-platform using system default player."""
    system = platform.system()
    if system == "Windows":
        os.startfile(filename)
    elif system == "Darwin":  # macOS
        os.system(f"afplay '{filename}'")
    else:  # Slackware Linux / other
        # Try aplay, ffplay, or mpv
        if os.system(f"aplay '{filename}'") != 0:
            if os.system(f"ffplay -nodisp -autoexit -loglevel quiet '{filename}'") != 0:
                print(f"Please open {filename} to play audio manually.")

def text_to_speech(text, lang="en", voice="af_heart"):
    if lang not in SUPPORTED_LANGS:
        print(f"Language '{lang}' not supported. Falling back to English.")
        lang = "en"

    pipeline = PIPELINES[lang]

    generator = pipeline(text, voice=voice, speed=1, split_pattern=r"\n+")

    for i, (gs, ps, audio) in enumerate(generator):
        filename = f"tts_output_{i}.wav"
        sf.write(filename, audio, 24000)
        print(f"Saved: {filename}")
        play_audio(filename)

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

def speak_gpt_response(text, lang="en", voice="af_heart"):
    text_to_speech(text, lang=lang, voice=voice)

# Example usage
if __name__ == "__main__":
    lang = choose_language()
    sample_text = "Hello! This is a test of Kokoro TTS on desktop."
    speak_gpt_response(sample_text, lang=lang)
