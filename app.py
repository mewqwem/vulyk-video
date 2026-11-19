"""Viewer for the series, part by part.  Usage: python app.py  ->  open http://localhost:8765

Read-only: every folder in parts/ is one part (lines.py + scene.html + whatever was generated there).
Shows the live scene preview with a timeline, the script with the running balance, and finished videos.
"""
import importlib.util, json, os
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

HERE = os.path.dirname(os.path.abspath(__file__))
PARTS = os.path.join(HERE, "parts")
PORT = int(os.environ.get("PORT", "8765"))
START_BALANCE = 1500000


def part_ids():
    ids = [d for d in os.listdir(PARTS) if os.path.exists(os.path.join(PARTS, d, "lines.py"))]
    return sorted(ids, key=lambda d: (len(d), d))


def load_lines(pid):
    path = os.path.join(PARTS, pid, "lines.py")
    spec = importlib.util.spec_from_file_location(f"lines_{pid}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def groups_from(phrases, maxw=3):  # same as render.py
    groups = []
    for ph in phrases:
        ws = ph["words"]
        for i in range(0, len(ws), maxw):
            chunk = ws[i:i + maxw]
            groups.append({"start": chunk[0]["s"], "words": chunk})
    for i, g in enumerate(groups):
        g["end"] = groups[i + 1]["start"] if i + 1 < len(groups) else phrases[-1]["e"] + 0.4
    return groups


def videos(d):
    vs = [f for f in os.listdir(d) if f.endswith(".mp4") and not f.endswith(".tmp.mp4") and f != "silent.mp4"]
    return sorted(vs, key=lambda f: os.path.getmtime(os.path.join(d, f)), reverse=True)


def part_info(pid):
    d = os.path.join(PARTS, pid)
    m = load_lines(pid)
    n = len(m.LINES)
    start = getattr(m, "START", START_BALANCE)
    spent = sum(a for l in m.LINES for _f, a in l[3])
    durs_ok = False
    if os.path.exists(os.path.join(d, "durs.json")):
        dd = json.load(open(os.path.join(d, "durs.json")))
        durs_ok = len(dd) == n and all(x > 0 for x in dd)
    return {"id": pid, "title": getattr(m, "TITLE", pid), "lines": n, "start": start, "end": start - spent,
            "voiced": durs_ok, "videos": videos(d)}


def timing(pid):
    d = os.path.join(PARTS, pid)
    m = load_lines(pid)
    n = len(m.LINES)
    durs = align = None
    real = False
    if os.path.exists(os.path.join(d, "durs.json")):
        dd = json.load(open(os.path.join(d, "durs.json")))
        if len(dd) == n and all(x > 0 for x in dd):
            durs, real = dd, True
            ap = os.path.join(d, "align.json")
            if os.path.exists(ap):
                al = json.load(open(ap))
                align = al if len(al) == n else None
    if durs is None:
        durs = [len(l[0].replace("*", "")) / 14 for l in m.LINES]
    T = m.build(durs, align=align)
    T["groups"] = groups_from(T["phrases"])
    T["real"] = real
    T["voice"] = real and os.path.exists(os.path.join(d, "voice.wav"))
    T["lines"] = [{"cap": l[0], "scene": l[2], "ded": l[3]} for l in m.LINES]
    T["start"] = getattr(m, "START", START_BALANCE)
    return T


class H(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=HERE, **k)

    def log_message(self, *a):
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def send_json(self, obj, code=200):
        b = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        u = urlparse(self.path)
        try:
            if u.path in ("/", "/index.html"):
                self.path = "/studio.html"
                return super().do_GET()
            if u.path == "/api/parts":
                return self.send_json([part_info(p) for p in part_ids()])
            if u.path == "/api/timing":
                pid = parse_qs(u.query).get("part", [""])[0]
                if pid not in part_ids():
                    return self.send_json({"error": "немає такої частини"}, 404)
                return self.send_json(timing(pid))
        except Exception as e:
            return self.send_json({"error": f"{type(e).__name__}: {e}"}, 500)
        # static: only the pages and files inside parts/, voice_samples/, fonts/
        if u.path in ("/studio.html", "/voices.html") or (u.path.startswith(("/parts/", "/voice_samples/", "/fonts/")) and ".." not in u.path and "/." not in u.path):
            if self.headers.get("Range") and u.path.endswith((".mp4", ".wav", ".mp3")):
                return self.send_range(os.path.join(HERE, u.path.lstrip("/")))
            return super().do_GET()
        self.send_error(404)

    def send_range(self, path):  # lets the browser seek in videos and audio
        if not os.path.isfile(path):
            return self.send_error(404)
        size = os.path.getsize(path)
        a, _, b = self.headers["Range"].replace("bytes=", "").partition("-")
        start = int(a) if a else max(0, size - int(b))
        end = min(int(b), size - 1) if a and b else size - 1
        if start >= size:
            self.send_response(416); self.send_header("Content-Range", f"bytes */{size}"); self.end_headers(); return
        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(end - start + 1))
        self.end_headers()
        with open(path, "rb") as f:
            f.seek(start)
            left = end - start + 1
            try:
                while left > 0:
                    chunk = f.read(min(1 << 20, left))
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    left -= len(chunk)
            except (BrokenPipeError, ConnectionResetError):
                pass


if __name__ == "__main__":
    print(f"Перегляд: http://localhost:{PORT}")
    ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
