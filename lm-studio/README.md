
**This is for Slackware Current but it will work in any Linux Desktop run LM-STUDIO.AppImage**<br>
** You can have 100% offline TTS from your lmstudio promt**

> REQUIRED: lm-studio.AppImage0.3.24-6 and  koroko `pip install -q kokoro>=0.9.2 soundfile`
>

General speaking scripts use:
```
import time
import json
from pathlib import Path
import threading
import sys
import platform
from kokoro import KPipeline
import soundfile as sf

```


### HOWTO

1. Download latest pre-release of project or clone repo.
2. Change to lm-studio folder and command: `python3 tts_watcher.py`
3. Start chatting with a model in your LM-STUDIO Gui (AppImage)

Note: 
- First time run if old convertations exists in your lm-studio .case it might start reading them even if lm-studio is off
- Its better first time to start with clean lmstudio convertations case.
- In my end with **python3.12** and lm-studio.AppImage-**0.3.24-6** works fine.




