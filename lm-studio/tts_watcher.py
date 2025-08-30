#!/usr/bin/env python3
import time
import json
from pathlib import Path
import threading
import sys

sys.path.insert(0, ".")
from local_tts import speak_gpt_response, choose_language

CONVO_DIR = Path.home() / ".lmstudio/conversations"

current_lang = "en"
spoken_messages = set()
spoken_steps = {}

def get_latest_convo_file():
    files = list(CONVO_DIR.glob("*.conversation.json"))
    if not files:
        return None
    # return the most recently modified conversation file
    return max(files, key=lambda f: f.stat().st_mtime)

def get_latest_text(convo_file):
    if not convo_file.exists():
        return []

    try:
        with convo_file.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[TTS] Failed to read JSON: {e}")
        return []

    texts_to_speak = []

    for msg in data.get("messages", []):
        for v in msg.get("versions", []):
            role = v.get("role")
            if role == "user":
                for c in v.get("content", []):
                    if c.get("type") == "text":
                        text = c.get("text", "")
                        if text not in spoken_messages:
                            texts_to_speak.append(text)
                            spoken_messages.add(text)
            elif role == "assistant":
                for step in v.get("steps", []):
                    step_id = step.get("stepIdentifier")
                    full_text = ""
                    for c in step.get("content", []):
                        if c.get("type") == "text" and not c.get("isStructural", False):
                            text = c.get("text", "")
                            for token in ["<|start|>assistant<|channel|>final<|message|>", "<|end|>", "<|return|>"]:
                                text = text.replace(token, "")
                            full_text += text

                    if full_text.strip():
                        spoken_chars = spoken_steps.get(step_id, 0)
                        new_text = full_text[spoken_chars:]
                        if new_text.strip():
                            texts_to_speak.append(new_text.strip())
                            spoken_steps[step_id] = len(full_text)

    return texts_to_speak

def watcher():
    print(f"[TTS] Watching {CONVO_DIR}")
    last_mtime = 0
    while True:
        try:
            convo_file = get_latest_convo_file()
            if convo_file is None:
                time.sleep(1)
                continue

            mtime = convo_file.stat().st_mtime
            if mtime != last_mtime:
                last_mtime = mtime
                texts = get_latest_text(convo_file)
                for t in texts:
                    try:
                        speak_gpt_response(t, lang=current_lang)
                    except Exception as e:
                        print(f"[TTS] Failed to speak: {e}")
            time.sleep(0.5)
        except KeyboardInterrupt:
            print("\n[TTS] Exiting.")
            break
        except Exception as e:
            print(f"[TTS] Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    watcher_thread = threading.Thread(target=watcher, daemon=True)
    watcher_thread.start()

    # live language switching (beta option NOT tested with koroko)
    # And tbh I think its wrong idea its better to do this from local_tts...
    while True:
        try:
            cmd = input()
            if cmd.startswith("/lang"):
                parts = cmd.strip().split()
                if len(parts) > 1:
                    current_lang = choose_language(parts[1])
        except KeyboardInterrupt:
            print("\n[TTS] Exiting main thread.")
            break
