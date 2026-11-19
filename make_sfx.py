"""Synthesises the sound effects into sfx/*.wav (pure Python, no samples, no licences).  Usage: python3 make_sfx.py"""
import math, os, random, struct, wave

SR = 44100
HERE = os.path.dirname(os.path.abspath(__file__))
random.seed(7)


def save(name, x, gain=0.8):
    peak = max(1e-9, max(abs(v) for v in x))
    os.makedirs(os.path.join(HERE, "sfx"), exist_ok=True)
    with wave.open(os.path.join(HERE, "sfx", name + ".wav"), "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(b"".join(struct.pack("<h", int(v / peak * gain * 32767)) for v in x))


def buf(sec): return [0.0] * int(sec * SR)


def add(x, t0, y, g=1.0):
    i0 = int(t0 * SR)
    for i, v in enumerate(y):
        if i0 + i < len(x): x[i0 + i] += v * g


def bell(f, sec, decay, harm=((1, 1), (2.76, .35), (5.4, .15))):
    return [sum(a * math.sin(2 * math.pi * f * m * i / SR) for m, a in harm) * math.exp(-i / SR * decay) *
            min(1, i / (SR * .002)) for i in range(int(sec * SR))]


def noise(sec, decay, smooth=1):
    out, prev = [], 0.0
    for i in range(int(sec * SR)):
        prev += (random.uniform(-1, 1) - prev) / smooth
        out.append(prev * math.exp(-i / SR * decay))
    return out


def glide(f0, f1, sec, decay=0, shape=None):
    out, ph = [], 0.0
    n = int(sec * SR)
    for i in range(n):
        k = i / n
        ph += 2 * math.pi * (f0 + (f1 - f0) * k) / SR
        env = shape(k) if shape else math.sin(math.pi * k)
        out.append(math.sin(ph) * env * math.exp(-i / SR * decay))
    return out


# money in: two bright bells + a little "ching" of coins
x = buf(1.0); add(x, 0, bell(1568, .9, 6)); add(x, .09, bell(2093, .9, 5), .9)
for k in range(5): add(x, .02 + k * .045, noise(.06, 60), .25)
save("cash_in", x)

# money out: soft falling tone + coins sliding away
x = buf(.7); add(x, 0, glide(820, 260, .45), .9)
for k in range(4): add(x, .05 + k * .08, noise(.05, 70), .12 * (1 - k * .2))
save("cash_out", x, .6)

# pop
save("pop", glide(380, 900, .07, shape=lambda k: math.sin(math.pi * k) ** .5), .5)

# whoosh: smoothed noise with a swell
n = noise(.45, 0, smooth=6); save("whoosh", [v * math.sin(math.pi * i / len(n)) ** 2 for i, v in enumerate(n)], .45)

# phone notification
x = buf(.6); add(x, 0, bell(1318, .5, 9, ((1, 1),))); add(x, .11, bell(1975, .45, 9, ((1, 1),)), .8); save("notify", x, .55)

# rubber stamp: low thump + paper slap
x = buf(.4); add(x, 0, glide(110, 55, .18, shape=lambda k: math.exp(-k * 5))); add(x, 0, noise(.08, 50, 2), .5); save("stamp", x, .8)

# three knocks on a wooden door
x = buf(1.2)
for k, t in enumerate((0, .28, .56)):
    add(x, t, glide(170, 90, .12, shape=lambda q: math.exp(-q * 8))); add(x, t, noise(.03, 120, 3), .6)
save("knock", x, .9)

print("sfx:", sorted(os.listdir(os.path.join(HERE, "sfx"))))
