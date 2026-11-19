TITLE = "Частина 5 · Дах"
START = 190000  # balance at the end of part 4
VOICE_SPEED = 1.1
# other voices: CAST name -> ElevenLabs voice_id (None = narrator voice); VOICED_BY line index -> CAST name
CAST = {"vlad": {"voice": "GVAs5c0aXpTTBsFQ9emv", "settings": {"stability": 0.3, "style": 0.6}}}  # Nestor Lipich, energetic (author 2026-11-13)
VOICED_BY = {7: "vlad", 14: "vlad", 15: "vlad", 16: "vlad"}
# (caption text, tts text, scene key, money [(fraction_of_line, amount)]; negative amount = income)
LINES = [
 ('380\xa0000 — стільки коштує дах над нашим баром. А в нас 190\xa0000.', "Триста вісімдесят тисяч — стільки коштує дах над нашим баром. А в нас — сто дев'яносто.", 'h1', []),
 ('Покрівельник лізе на дах і довго мовчить.', 'Покрі́вельник лізе на дах і довго мовчить.', 'r1', []),
 ('«Черепицю міняти всю. І тільки таку, як була 130 років тому».', '«Черепицю міняти всю. І тільки таку, як була сто тридцять років тому».', 'r2', []),
 ('Будинок під охороною: потрібен дозвіл міста і проєкт. 25\xa0000.', "Будинок під охороною: потрібен дозвіл міста і проєкт. Двадцять п'ять тисяч.", 'r3', [(0.88, 25000)]),
 ('А поки — відра під протікання і плівка на стелю. Ще 3\xa0000.', 'А поки — відра під протікання і плівка на стелю. Ще три тисячі.', 'r4', [(0.9, 3000)]),
 ('Того вечора ми з Владом уперше посварились.', 'Того вечора ми з Владом уперше посварились.', 'q1', []),
 ('Я кажу: «Ти підписав договір і не прочитав».', 'Я кажу: «Ти підписав договір і не прочитав».', 'q2', []),
 ('«А медовуху не з реєстру хто взяв? Штраф — теж я?»', '«А медовуху не з реєстру хто взяв? Штраф — теж я?»', 'q3', []),
 ('Ми кричали так, що Ігор вивів останніх гостей.', 'Ми кричали так, що Ігор вивів останніх гостей.', 'q4', []),
 ('І я сказав те, що думав від першого дня: «Я вклав півтора мільйона. Ти — 400 тисяч. А ділимо навпіл».', 'І я сказав те, що думав від першого дня. «Я вклав півтора мільйона. Ти — чотириста тисяч. А ділимо навпіл».', 'q5', []),
 ('Влад мовчки пішов.', 'Влад мо́вчки пішов.', 'q6', []),
 ('Три дні дощ. Чотири столики під відрами ми не продаємо.', 'Три дні дощ. Чотири столики під відрами ми не продаємо.', 'w1', []),
 ('Каса за тиждень — 95\xa0000. Мінус медовуха, зарплати, податок і світло — 54\xa0500.', "Каса за тиждень — дев'яносто п'ять тисяч. Мінус медовуха, зарплати, податок і світло — п'ятдесят чотири з половиною.", 'w2', [(0.35, -95000), (0.55, 25000), (0.62, 17000), (0.69, 5000), (0.76, 7500)]),
 ('У понеділок Влад приходить з папкою з банку.', 'У понеділок Влад приходить з папкою з банку.', 'v1', []),
 ('«Кредит на мене. 400 тисяч — у бар».', '«Кредит на мене. Чотириста тисяч — у бар».', 'v2', [(0.75, -400000)]),
 ('«Різницю до півтора мільйона доплачу зі своєї частки прибутку. Тоді буде чесно».', '«Різницю до півтора мільйона доплачу зі своєї частки прибутку. Тоді буде чесно».', 'v3', []),
 ('«Я не прочитав договір. Значить, дах — мій».', '«Я не прочитав договір. Значить, дах — мій».', 'v4', []),
 ('Платить він сам, 18 тисяч на місяць. Ми не обіймались. Просто поїхали по черепицю.', 'Платить він сам, вісімнадцять тисяч на місяць. Ми не обіймались. Просто поїхали по черепицю.', 'v5', []),
 ('Матеріали — 220\xa0000. Аванс бригаді — 80\xa0000. І бухгалтер — 4\xa0000.', 'Матеріали — двісті двадцять тисяч. Аванс бригаді — вісімдесят тисяч. І бухгалтер — чотири тисячі.', 'b1', [(0.3, 220000), (0.68, 80000), (0.95, 4000)]),
 ("У п'ятницю покрівельники знімають стару черепицю.", "У п'ятницю покрі́вельники знімають стару черепицю.", 'f1', []),
 ('«Крокви гнилі. Ще 150 тисяч. Або дах просто впаде».', "«Кро́кви гнилі. Ще сто п'ятдесят тисяч. Або дах просто впаде».", 'f2', []),
 ('На рахунку 298\xa0500. Але попереду решта бригаді, оренда й кредит.', "На рахунку двісті дев'яносто вісім з половиною тисяч. Але попереду — решта бригаді, оренда й кредит.", 'f3', []),
 ('Того ж вечора за стійку сідає наш постійний гість Роман. Він чув про дах.', 'Того ж вечора за сті́йку сідає наш постійний гість Роман. Він чув про дах.', 'f4', []),
 ('«Даю 200 тисяч одразу. Натомість — мій столик назавжди і медовуха тричі на тиждень безкоштовно».', '«Даю двісті тисяч одразу. Натомість — мій столик назавжди і медовуха тричі на тиждень безкоштовно».', 'f5', []),
 ('Цю ідею, до речі, запропонував один із вас у коментарях.', 'Цю ідею, до речі, запропонував один із вас у коментарях.', 'f6', []),
 ('Брати гроші і віддати столик назавжди? Чи шукати 150 тисяч самим? Пиши в коментарях. Шоста частина — «Гість».', "Брати гроші і віддати столик назавжди? Чи шукати сто п'ятдесят тисяч самим? Пиши в коментарях. Шоста частина — «Гість».", 'f7', []),
]
# sound cues: (scene key, word index or start of a word, sfx name)
SFX = [("v2", "кредит", "stamp"), ("f2", "крокви", "stamp")]
GAP = 0.22

def _norm(w):
    return ''.join(c for c in w.lower().replace('’', "'") if c.isalnum() or c == "'")


def map_words(cap_words, tts_words, al):
    """Caption word times from the spoken word times, also when a number in the caption ("70 000")
    is spoken as several words ("сімдесят тисяч"). Returns [[s, e], ...] per caption word, or None."""
    if len(tts_words) != len(al):
        return None
    cn, tn = [_norm(w) for w in cap_words], [_norm(w) for w in tts_words]
    out, i, j = [], 0, 0
    while i < len(cn):
        if j < len(tn) and cn[i] == tn[j]:
            out.append(list(al[j])); i += 1; j += 1
            continue
        i2 = i  # run of caption words that are not spoken as written (numbers)
        while i2 < len(cn) and not any(cn[i2] == x for x in tn[j:j + 1]):
            i2 += 1
            if i2 < len(cn) and cn[i2] in tn[j:]:
                break
        nxt = cn[i2] if i2 < len(cn) else None
        j2 = tn.index(nxt, j) if nxt is not None and nxt in tn[j:] else len(tn)
        if j2 == j:
            return None
        s, e = al[j][0], al[j2 - 1][1]
        k = i2 - i
        out += [[s + (e - s) * m / k, s + (e - s) * (m + 1) / k] for m in range(k)]
        i, j = i2, j2
    return out if j == len(tn) else None


def build(durations, lead=0.3, align=None):
    # align: optional list (per line) of [[start, end], ...] spoken word times from the voice
    t = lead
    phrases = []
    for n, ((line, tts, scene, ded), d) in enumerate(zip(LINES, durations)):
        words = line.split(' ')
        al = align[n] if align else None
        if al and len(al) != len(words):
            al = map_words(words, tts.replace('+', '').split(), al)
        if al and len(al) == len(words):  # exact timings from the voice
            ws = [{"text": w.strip('*'), "hl": w.startswith('*'), "s": round(t + a[0], 3), "e": round(t + a[1], 3)}
                  for w, a in zip(words, al)]
            phrases.append({"text": line.replace('*', ''), "s": round(t, 3), "e": round(t + d, 3), "words": ws,
                            "scene": scene, "ded": [[round(t + f * d, 3), a] for f, a in ded]})
            t += d + GAP
            continue
        lens = [len(w.strip('*')) + 2 for w in words]
        tot = sum(lens)
        ws, c = [], t
        for w, L in zip(words, lens):
            dd = d * L / tot
            ws.append({"text": w.strip('*'), "hl": w.startswith('*'), "s": round(c, 3), "e": round(c + dd, 3)})
            c += dd
        phrases.append({"text": line.replace('*', ''), "s": round(t, 3), "e": round(t + d, 3), "words": ws,
                        "scene": scene, "ded": [[round(t + f * d, 3), a] for f, a in ded]})
        t += d + GAP
    return {"phrases": phrases, "duration": round(t + 1.2, 2)}

if __name__ == "__main__":
    import json, sys
    durs = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else [len(l[0]) / 14 for l in LINES]
    align = json.load(open(sys.argv[2])) if len(sys.argv) > 2 else None
    json.dump(build(durs, align=align), open("timing.json", "w"), ensure_ascii=False, indent=1)
    print(json.load(open("timing.json"))["duration"])
