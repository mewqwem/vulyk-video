"""Send a finished part to Telegram through our bot (token in .env, never printed).

  python3 tg_post.py ids                      chats the bot has seen (to find TG_ME_CHAT_ID / TG_CHANNEL_ID)
  python3 tg_post.py me parts/part4           video + post_tg.txt to your private chat with the bot (a draft)
  python3 tg_post.py channel parts/part4      the same into the channel — only after the author said yes
  python3 tg_post.py me parts/part4 --file    send the video as a document (no Telegram re-compression)
  python3 tg_post.py text parts/part4/post_tiktok.txt   a text file to your chat with the bot

.env: TG_BOT_TOKEN=..., TG_ME_CHAT_ID=..., TG_CHANNEL_ID=...
The part folder holds partN.mp4 and post_tg.txt (caption, max 1024 chars). Bot API upload limit is 50 MB.
"""
import json, os, sys, uuid, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.abspath(__file__))


def env():
    vals = {}
    for line in open(os.path.join(ROOT, ".env"), encoding="utf-8"):
        if "=" in line and not line.lstrip().startswith("#"):
            k, v = line.split("=", 1)
            vals[k.strip()] = v.strip().strip('"').strip("'")
    return vals


E = env()
TOKEN = E.get("TG_BOT_TOKEN")
if not TOKEN:
    sys.exit("TG_BOT_TOKEN не знайдено в .env")
API = f"https://api.telegram.org/bot{TOKEN}/"


def call(method, fields=None, files=None):
    if files:
        b = uuid.uuid4().hex
        body = b""
        for k, v in (fields or {}).items():
            body += f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
        for k, path in files.items():
            body += (f'--{b}\r\nContent-Disposition: form-data; name="{k}"; filename="{os.path.basename(path)}"\r\n'
                     f"Content-Type: application/octet-stream\r\n\r\n").encode() + open(path, "rb").read() + b"\r\n"
        body += f"--{b}--\r\n".encode()
        req = urllib.request.Request(API + method, data=body, headers={"Content-Type": f"multipart/form-data; boundary={b}"})
    else:
        req = urllib.request.Request(API + method, data=json.dumps(fields or {}).encode(),
                                     headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:  # Telegram explains the problem in the body; the URL (with the token) is not printed
        sys.exit("Telegram: " + json.load(e).get("description", str(e.code)))


def ids():
    me = call("getMe")["result"]
    print("бот:", "@" + me["username"])
    seen = {}
    for u in call("getUpdates")["result"]:
        for key in ("message", "channel_post", "my_chat_member", "edited_channel_post"):
            c = (u.get(key) or {}).get("chat")
            if c:
                seen[c["id"]] = (c.get("type"), c.get("title") or c.get("first_name") or c.get("username"))
    for cid, (typ, name) in seen.items():
        print(f"{cid}\t{typ}\t{name}")
    if not seen:
        print("Поки нічого: напиши боту /start і/або опублікуй щось у каналі, де бот адмін, тоді запусти ще раз.")


def send(where, part, as_file):
    chat = E.get("TG_ME_CHAT_ID" if where == "me" else "TG_CHANNEL_ID")
    if not chat:
        sys.exit(f"{'TG_ME_CHAT_ID' if where == 'me' else 'TG_CHANNEL_ID'} не знайдено в .env")
    name = os.path.basename(os.path.normpath(part))
    video = os.path.join(part, name + ".mp4")
    cap_path = os.path.join(part, "post_tg.txt")
    caption = open(cap_path, encoding="utf-8").read().strip() if os.path.exists(cap_path) else ""
    if len(caption) > 1024:
        sys.exit(f"підпис задовгий: {len(caption)} > 1024")
    mb = os.path.getsize(video) / 1e6
    if mb > 50:
        sys.exit(f"{video}: {mb:.1f} МБ, бот може максимум 50")
    if as_file:
        r = call("sendDocument", {"chat_id": chat, "caption": caption}, {"document": video})
    else:
        r = call("sendVideo", {"chat_id": chat, "caption": caption, "supports_streaming": "true",
                               "width": "1080", "height": "1920"}, {"video": video})
    print("надіслано:", where, video, f"{mb:.1f} МБ", "message_id", r["result"]["message_id"])


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if not a or a[0] == "ids":
        ids()
    elif a[0] == "text" and len(a) == 2:  # a text file to my chat, e.g. post_tiktok.txt
        r = call("sendMessage", {"chat_id": E["TG_ME_CHAT_ID"], "text": open(a[1], encoding="utf-8").read().strip()})
        print("надіслано текст, message_id", r["result"]["message_id"])
    elif a[0] in ("me", "channel") and len(a) == 2:
        send(a[0], a[1], "--file" in sys.argv)
    else:
        print(__doc__)
