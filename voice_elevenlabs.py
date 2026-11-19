"""Generate voiceover for every line in lines.py via ElevenLabs (with word timestamps).

Needs env vars:
  ELEVENLABS_API_KEY  - your API key
  ELEVENLABS_VOICE_ID - voice id (copy from the ElevenLabs voice library)
Usage: python voice_elevenlabs.py parts/part1 [3,7]
Writes into the part folder: audio/l_<n>.wav, durs.json, align.json
"""
import base64, json, os, subprocess, sys, urllib.request
os.chdir(sys.argv[1]); sys.path.insert(0, os.getcwd())
from lines import LINES

KEY = os.environ["ELEVENLABS_API_KEY"]
VOICE = os.environ["ELEVENLABS_VOICE_ID"]
MODEL = os.environ.get("ELEVENLABS_MODEL", "eleven_multilingual_v2")
SPEED = float(os.environ.get("ELEVENLABS_SPEED", "1.08"))
os.makedirs("audio", exist_ok=True)


def tts(text):
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps",
        data=json.dumps({"text": text, "model_id": MODEL,
                         "voice_settings": {"stability": 0.45, "similarity_boost": 0.8, "speed": SPEED}}).encode(),
        headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def words_from_alignment(al):
    chars, st, en = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    words, cur = [], None
    for c, s, e in zip(chars, st, en):
        if c.isspace():
            if cur: words.append(cur); cur = None
            continue
        if cur is None: cur = [s, e]
        else: cur[1] = e
    if cur: words.append(cur)
    return words


only = set(int(x) for x in sys.argv[2].split(",")) if len(sys.argv) > 2 else None  # e.g. "3,7" to redo some lines
durs = json.load(open("durs.json")) if only and os.path.exists("durs.json") else [0] * len(LINES)
align = json.load(open("align.json")) if only and os.path.exists("align.json") else [None] * len(LINES)
for i, (_cap, say, _scene, _ded) in enumerate(LINES):
    if only and i not in only: continue
    text = say.replace("+", "")  # stress marks are only for the offline model
    res = tts(text)
    mp3 = f"audio/l_{i}.mp3"
    open(mp3, "wb").write(base64.b64decode(res["audio_base64"]))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp3, "-ar", "44100", "-ac", "1", f"audio/l_{i}.wav"], check=True)
    durs[i] = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                             "-of", "csv=p=0", f"audio/l_{i}.wav"]))
    align[i] = words_from_alignment(res.get("normalized_alignment") or res["alignment"])
    print(f"{i:2d} {durs[i]:.2f}s  {text}")
json.dump(durs, open("durs.json", "w"))
json.dump(align, open("align.json", "w"))
