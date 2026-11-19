"""Timings -> voice track -> render -> final mp4.  Usage: python build.py parts/part1 [output.mp4]
                                                    python build.py parts/part1 --voice-only   (just voice.wav)
Everything is read from and written to the part folder."""
import json, os, subprocess, sys

TOOLS = os.path.dirname(os.path.abspath(__file__))
args = [a for a in sys.argv[1:] if not a.startswith("--")]
voice_only = "--voice-only" in sys.argv
os.chdir(args[0])
out = args[1] if len(args) > 1 else os.path.basename(os.getcwd()) + ".mp4"
subprocess.run([sys.executable, "lines.py", "durs.json", "align.json"], check=True)
T = json.load(open("timing.json"))
n = len(T["phrases"])

# sound effects: money in/out on every deduction, a whoosh between sections, extra cues from SFX in lines.py
# (SFX = [(scene_key, word_index, "name"), ...]; names are files in sfx/, made by make_sfx.py)
SFX_DIR = os.path.join(TOOLS, "sfx")
VOL = {"cash_in": .33, "cash_out": .27, "whoosh": .18, "pop": .2, "notify": .27, "stamp": .33, "knock": .55}  # quieter (author, 2026-11-13)
events = []
for k, p in enumerate(T["phrases"]):
    for td, a in p["ded"]:
        events.append((td - .05, "cash_in" if a < 0 else "cash_out"))
    if k and p["scene"][0] != T["phrases"][k - 1]["scene"][0]:
        events.append((p["s"] - .3, "whoosh"))
try:
    from importlib import util
    spec = util.spec_from_file_location("lines_sfx", "lines.py"); mod = util.module_from_spec(spec); spec.loader.exec_module(mod)
    by_key = {p["scene"]: p for p in T["phrases"]}
    for key, wi, name in getattr(mod, "SFX", []):
        ws = by_key[key]["words"]
        if isinstance(wi, str):  # start of a word, e.g. "беремо"
            norm = lambda w: "".join(c for c in w.lower() if c.isalnum() or c == "'")
            wi = next((k for k, w in enumerate(ws) if norm(w["text"]).startswith(wi)), 0)
        events.append((ws[min(wi, len(ws) - 1)]["s"], name))
except FileNotFoundError:
    pass
# every element that pops onto the screen gets a sound (times collected from scene.html by render.py --pops)
subprocess.run([sys.executable, os.path.join(TOOLS, "render.py"), "timing.json", "--pops"], check=True)
for t, kind in json.load(open("pops.json")):
    if all(abs(t - te) > .18 for te, _ in events):  # skip if money / whoosh / a manual cue already sounds there
        events.append((t, kind))
events = sorted((t, nm) for t, nm in events if os.path.exists(os.path.join(SFX_DIR, nm + ".wav")))
dedup = []
for t, nm in events:  # several things popping at the same instant = one sound
    if dedup and abs(t - dedup[-1][0]) < .08 and nm == dedup[-1][1]:
        continue
    dedup.append((t, nm))
events = dedup

inputs, filt = [], []
for i, p in enumerate(T["phrases"]):
    inputs += ["-i", f"audio/l_{i}.wav"]
    ms = int(p["s"] * 1000)
    filt.append(f"[{i}]adelay={ms}|{ms}[d{i}]")
for j, (t, nm) in enumerate(events):
    k = n + j
    inputs += ["-i", os.path.join(SFX_DIR, nm + ".wav")]
    ms = max(0, int(t * 1000))
    filt.append(f"[{k}]volume={VOL.get(nm, .4)},adelay={ms}|{ms}[d{k}]")
m = n + len(events)
mix = "".join(f"[d{i}]" for i in range(m)) + \
      f"amix=inputs={m}:normalize=0,apad,atrim=0:{T['duration']},loudnorm=I=-14:TP=-1.5[a]"
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(filt) + ";" + mix,
                "-map", "[a]", "-ar", "44100", "-ac", "2", "voice.wav"], check=True)
print(f"звуків: {len(events)}")
if voice_only:
    sys.exit(print("voice.wav ready,", T["duration"], "s"))

subprocess.run([sys.executable, os.path.join(TOOLS, "render.py"), "timing.json", "silent.mp4"], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "silent.mp4", "-i", "voice.wav", "-map", "0:v", "-map", "1:a",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out], check=True)
print("ready:", os.path.abspath(out))
