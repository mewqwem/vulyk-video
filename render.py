import json, subprocess, sys, os, asyncio
from playwright.async_api import async_playwright

HERE = os.getcwd()  # the part folder (holds scene.html)
FPS = 30

def groups_from(phrases, maxw=3):
    groups = []
    for ph in phrases:
        ws = ph["words"]
        for i in range(0, len(ws), maxw):
            chunk = ws[i:i + maxw]
            groups.append({"start": chunk[0]["s"], "words": chunk})
    for i, g in enumerate(groups):
        g["end"] = groups[i + 1]["start"] if i + 1 < len(groups) else phrases[-1]["e"] + 0.4
    return groups

async def main(timing_path, out_path, snaps=None):
    T = json.load(open(timing_path))
    phrases = T["phrases"]
    P = [{"s": p["s"], "e": p["e"]} for p in phrases]
    G = groups_from(phrases)
    W = [w for p in phrases for w in p["words"]]
    duration = T["duration"]
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        await pg.goto("file://" + os.path.join(HERE, "scene.html"))
        await pg.evaluate("([P,W,G,PH])=>{window.P=P;window.WORDS=W;window.GROUPS=G;window.PH=PH;}", [P, W, G, phrases])
        await pg.evaluate("document.fonts.ready")
        if out_path == "--pops":  # collect the start time of every pop()/stamp() in the scene -> pops.json
            found = set()
            for ph in phrases:
                await pg.evaluate("window.__pops=[]")
                await pg.evaluate(f"render({ph['e'] - 0.02})")
                for t0, kind in await pg.evaluate("window.__pops"):
                    if t0 is not None and ph["s"] - 0.5 <= t0 <= ph["e"] + 0.3:
                        found.add((round(t0, 2), kind))
            json.dump(sorted(found), open(os.path.join(HERE, "pops.json"), "w"))
            await b.close(); print("pops:", len(found)); return
        if snaps:
            for t in snaps:
                await pg.evaluate(f"render({t})")
                await pg.screenshot(path=os.path.join(HERE, f"snap_{t:05.2f}.jpg"), type="jpeg", quality=85)
            await b.close(); return
        tmp = out_path[:-4] + ".tmp.mp4"
        ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg",
                               "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", tmp],
                              stdin=subprocess.PIPE)
        n = int(duration * FPS)
        for i in range(n):
            await pg.evaluate(f"render({i / FPS})")
            ff.stdin.write(await pg.screenshot(type="jpeg", quality=92))
        ff.stdin.close(); rc = ff.wait()
        await b.close()
        if rc == 0: os.replace(tmp, out_path)
        print("done", out_path, rc)

if __name__ == "__main__":
    snaps = [float(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else None
    asyncio.run(main(sys.argv[1], sys.argv[2], snaps))
