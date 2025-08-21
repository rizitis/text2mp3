#!/usr/bin/python3

# required `pip install gTTS`

import sys
import os
import shutil
import tempfile
from gtts import gTTS

def play_audio(filename, player=None):
    if player == "mpg123" or (player is None and shutil.which("mpg123")):
        os.system(f"mpg123 -q {filename}")
    elif player == "ffplay" or (player is None and shutil.which("ffplay")):
        os.system(f"ffplay -nodisp -autoexit -loglevel quiet {filename}")
    else:
        print("No supported audio player found (install mpg123 or ffmpeg).")

def text_to_speech(text, lang="en", player=None):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        filename = tmp.name
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)
    play_audio(filename, player)
    os.remove(filename)

if __name__ == "__main__":
    player = None
    filepath = None

    if len(sys.argv) > 1:
        if sys.argv[1] in ("mpg123", "ffplay"):
            player = sys.argv[1]
        else:
            filepath = sys.argv[1]
    if len(sys.argv) > 2:
        player = sys.argv[2]

    if filepath:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            print(f" Reading from {filepath}...\n")
            text_to_speech(text, player=player)
        except FileNotFoundError:
            print(f"File '{filepath}' not found!")

    print(" Text-to-Speech ready. Type text and press Enter.")
    print("Press Ctrl+C to quit.\n")

    try:
        while True:
            text = input("> ")
            if text.strip():
                text_to_speech(text, player=player)
    except KeyboardInterrupt:
        print("\n Exiting. Goodbye!")
