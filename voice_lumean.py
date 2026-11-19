"""Voiceover for a part via Lumean (ElevenLabs voices), with per-letter timings.

Usage:  python voice_lumean.py parts/part1          # whole text in ONE order (even intonation), then cut into lines
        python voice_lumean.py parts/part1 3,7      # redo only lines 3 and 7, one order per line
Reads LUMEAN_API_KEY and LUMEAN_TEMPLATE_ID from .env next to this script (voice is set in the template;
LUMEAN_VOICE_ID in .env overrides it).
Writes into the part folder: audio/l_<n>.wav, durs.json, align.json (and audio/whole.mp3/.json in whole mode)
"""
import json, os, subprocess, sys, time, urllib.error, urllib.request
from concurrent.futures import ThreadPoolExecutor

TOOLS = os.path.dirname(os.path.abspath(__file__))
BASE = "https://api.lumean.app/api/public"
PARALLEL = 4


def load_env():
    env = {}
    p = os.path.join(TOOLS, ".env")
    if os.path.exists(p):
        for ln in open(p, encoding="utf-8"):
            ln = ln.strip()
            if ln and not ln.startswith("#") and "=" in ln:
                k, v = ln.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    env.update({k: v for k, v in os.environ.items() if k.startswith("LUMEAN_")})
    return env


ENV = load_env()
KEY = ENV["LUMEAN_API_KEY"]
TEMPLATE = ENV["LUMEAN_TEMPLATE_ID"]
VOICE = ENV.get("LUMEAN_VOICE_ID")
SPEED = None  # VOICE_SPEED in a part's lines.py (e.g. 1.1) overrides the template speed for that part
VOICE_SETTINGS = {"stability": 0.6, "similarity_boost": 0.8, "style": 0, "use_speaker_boost": True}  # = template


def api(method, path, body=None):
    for attempt in range(8):
        req = urllib.request.Request(BASE + path, method=method,
                                     data=json.dumps(body, ensure_ascii=False).encode() if body is not None else None,
                                     headers={"X-API-KEY": KEY, "Content-Type": "application/json",
                                              "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)["data"]
        except urllib.error.HTTPError as e:
            txt = e.read().decode(errors="replace")
            if e.code in (429, 500, 502, 503) and attempt < 7:  # limits / temporary errors: wait and retry
                wait = int(e.headers.get("Retry-After") or 0) or 5 * (attempt + 1)
                print(f"  {e.code}, чекаю {wait} с … {txt[:120]}")
                time.sleep(wait)
                continue
            raise SystemExit(f"Lumean {method} {path}: HTTP {e.code} {txt[:400]}")


def download(path, dest):
    url = api("POST", "/storage/url", {"path": path})["url"]
    with urllib.request.urlopen(url, timeout=120) as r, open(dest, "wb") as f:
        f.write(r.read())


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


def order_tts(text, name, mp3, js, voice=None, settings=None):
    """One TTS order -> downloads the audio to mp3 and the timings (result.json) to js."""
    body = {"template_id": TEMPLATE, "input_text": text, "name": name}
    tts = {}
    if voice or VOICE:
        tts["voice_id"] = voice or VOICE
    if SPEED or settings:
        tts["voice_settings"] = {**VOICE_SETTINGS, **({"speed": SPEED} if SPEED else {}), **(settings or {})}
    if tts:
        body["config_override"] = {"tts_settings": tts}
    order = api("POST", "/orders", body)
    oid = order["id"]
    while order["status"] not in ("completed", "result_delivered", "failed", "compensated", "cancelled", "partially_completed"):
        time.sleep(3)
        order = api("GET", f"/orders/{oid}")
    res = order.get("result") or {}
    if order["status"] not in ("completed", "result_delivered") or not res.get("files"):
        raise SystemExit(f"{name}: замовлення {oid} {order['status']}: {res.get('user_message')}")
    download(res["files"][0], mp3)
    rj = next(p for p in res.get("service_files", []) if p.endswith("result.json"))
    download(rj, js)


def voice_whole(texts, part, ids=None):
    """Whole part in one order, then cut into lines by word timings (pauses between lines come from build.py)."""
    order_tts(" ".join(texts), f"{part} whole", "audio/whole.mp3", "audio/whole.json")
    words = words_from_alignment(json.load(open("audio/whole.json"))["alignment"])
    counts = [len(t.split()) for t in texts]
    if len(words) != sum(counts):
        raise SystemExit(f"слів у таймінгах {len(words)}, а в тексті {sum(counts)} — не можу розрізати")
    spans, k = [], 0
    for c in counts:
        spans.append(words[k:k + c]); k += c
    out = []
    for i, ws in enumerate(spans):
        prev_end = spans[i - 1][-1][1] if i else 0.0
        next_start = spans[i + 1][0][0] if i + 1 < len(spans) else ws[-1][1] + 0.5
        a = max(prev_end, ws[0][0] - 0.04)          # a hair before the first word
        b = min(next_start, ws[-1][1] + 0.08)       # let the last word ring out
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "audio/whole.mp3", "-ss", f"{a:.3f}", "-to", f"{b:.3f}",
                        "-af", "afade=t=in:d=0.01,areverse,afade=t=in:d=0.02,areverse",
                        "-ar", "44100", "-ac", "1", f"audio/l_{ids[i] if ids else i}.wav"], check=True)
        out.append((ids[i] if ids else i, round(b - a, 3), [[round(s - a, 3), round(e - a, 3)] for s, e in ws]))
    return out


def voice_line(i, text, part, voice=None):
    """voice: None, a voice_id, or {"voice": voice_id, "settings": {...}} (e.g. lower stability, more style)."""
    mp3, js = f"audio/l_{i}.mp3", f"audio/l_{i}.json"
    v, st = (voice.get("voice"), voice.get("settings")) if isinstance(voice, dict) else (voice, None)
    order_tts(text, f"{part} line {i}", mp3, js, v, st)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp3, "-ar", "44100", "-ac", "1", f"audio/l_{i}.wav"], check=True)
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                         "-of", "csv=p=0", f"audio/l_{i}.wav"]))
    return i, dur, words_from_alignment(json.load(open(js))["alignment"])


def main():
    os.chdir(sys.argv[1])
    sys.path.insert(0, os.getcwd())
    import lines as L
    from lines import LINES
    global SPEED
    SPEED = getattr(L, "VOICE_SPEED", None)
    part = os.path.basename(os.getcwd())
    os.makedirs("audio", exist_ok=True)
    only = set(int(x) for x in sys.argv[2].split(",")) if len(sys.argv) > 2 else None
    n = len(LINES)
    durs = json.load(open("durs.json")) if only and os.path.exists("durs.json") else [0] * n
    align = json.load(open("align.json")) if only and os.path.exists("align.json") else [None] * n
    durs = (durs + [0] * n)[:n]; align = (align + [None] * n)[:n]
    cast, by = getattr(L, "CAST", {}), getattr(L, "VOICED_BY", {})  # lines spoken by other characters
    todo = [(i, l[1].replace("+", "")) for i, l in enumerate(LINES) if not only or i in only]
    if only:
        print(f"{part}: переозвучую рядки {sorted(only)} окремо …")
        with ThreadPoolExecutor(PARALLEL) as ex:
            results = list(ex.map(lambda a: voice_line(a[0], a[1], part, cast.get(by.get(a[0]))), todo))
    else:
        narr = [(i, t) for i, t in todo if i not in by]
        print(f"{part}: озвучую текст оповідача одним замовленням ({len(narr)} рядків) …")
        results = voice_whole([t for _, t in narr], part, [i for i, _ in narr])
        others = [(i, t) for i, t in todo if i in by]
        if others:
            print(f"{part}: репліки героїв окремо: {[(i, by[i]) for i, _ in others]} …")
            with ThreadPoolExecutor(PARALLEL) as ex:
                results += list(ex.map(lambda a: voice_line(a[0], a[1], part, cast.get(by[a[0]])), others))
        results.sort()
    for i, d, w in results:
        durs[i], align[i] = d, w
        print(f"{i:2d} {d:5.2f} с  {LINES[i][1].replace('+', '')}")
    json.dump(durs, open("durs.json", "w"))
    json.dump(align, open("align.json", "w"))
    from lines import map_words
    exact = 0
    for (cap, tts, *_), a in zip(LINES, align):
        cw = cap.split(' ')
        m = a if a and len(a) == len(cw) else (a and map_words(cw, tts.replace('+', '').split(), a))
        exact += bool(m and len(m) == len(cw))
    print(f"готово: {sum(durs):.1f} с голосу; точні таймінги субтитрів у {exact}/{n} рядків")


if __name__ == "__main__":
    main()
