TITLE = "Підсумки · після 5 частини"
START = 0  # recap: the card counts money PUT IN (savings, loan, Vlad, Vlad's loan), not the balance; not a canon part
VOICE_SPEED = 1.1
CAST = {"vlad": {"voice": "GVAs5c0aXpTTBsFQ9emv", "settings": {"stability": 0.3, "style": 0.6}}}
VOICED_BY = {}
# (caption text, tts text, scene key, money [(fraction_of_line, amount)]; negative amount = money put in)
LINES = [
 ('2\xa0300\xa0000 гривень, два кредити і дах, якому 130 років.', 'Два мільйони триста тисяч гривень, два кредити і дах, якому сто тридцять років.', 'h1', []),
 ('Ось що таке наш бар через три місяці. Якщо ти тут уперше — за хвилину розкажу все.', 'Ось що таке наш бар через три місяці. Якщо ти тут уперше — за хвилину розкажу все.', 'h2', []),
 ('Я Назар. Сім років стояв за барною стійкою у Львові. А потім мій бар зник за одну ніч.', 'Я Назар. Сім років стояв за барною сті́йкою у Львові. А потім мій бар зник за одну ніч.', 'a1', []),
 ('Тож я вирішив відкрити свій. «Вулик» — бар, де є тільки медовуха.', 'Тож я вирішив відкрити свій. «Вулик» — бар, де є тільки медовуха.', 'a2', []),
 ("Півтора мільйона: 800 тисяч я збирав п'ять років, 700 — кредит.", "Півтора мільйона: вісімсот тисяч я збирав п'ять років, сімсот — кредит.", 'a3', [(0.5, -800000), (0.93, -700000)]),
 ("За місяць від них лишилось 35 тисяч.", "За місяць від них лишилось тридцять п'ять тисяч.", 's1', []),
 ('Урок перший: свою медовуху варити не можна — це виробництво. Купуємо в медоварні.', 'Урок перший. Свою медовуху варити не можна — це виробництво. Купуємо в медоварні.', 'l1', []),
 ('Потім прийшов Влад, мій друг. Вклав 400 тисяч і став співвласником — 50 на 50.', "Потім прийшов Влад, мій друг. Вклав чотириста тисяч і став співвласником — п'ятдесят на п'ятдесят.", 'v1', [(0.55, -400000)]),
 ('На відкритті двоє барменів просто не прийшли. Зарплату за місяць вони взяли наперед.', 'На відкритті двоє барменів просто не прийшли. Зарплату за місяць вони взяли наперед.', 's2', []),
 ('Урок другий: нічого наперед, усіх оформлюємо офіційно.', 'Урок другий. Нічого наперед, усіх оформлюємо офіційно.', 'l2', []),
 ('Потім я взяв дешеву медовуху в медоварні, якої немає в реєстрі. Штраф — 73\xa0500.', 'Потім я взяв дешеву медовуху в медоварні, якої немає в реєстрі. Штраф — сімдесят три з половиною тисячі.', 's3', []),
 ('Урок третій: перевіряй усіх, з ким працюєш. Це, до речі, порадили ви.', 'Урок третій. Перевіряй усіх, з ким працюєш. Це, до речі, порадили ви.', 'l3', []),
 ('А Влад підписав договір оренди, не дочитавши. Там був пункт: дах ремонтує орендар.', 'А Влад підписав договір оренди, не дочитавши. Там був пункт: дах ремонтує орендар.', 's4', []),
 ('Дах обійшовся більш ніж у пів мільйона. Влад узяв на себе ще один кредит.', 'Дах обійшовся більш ніж у пів мільйона. Влад узяв на себе ще один кредит.', 's5', [(0.93, -400000)]),
 ('Урок четвертий: дочитуй договори до кінця.', 'Урок четвертий. Дочитуй договори до кінця.', 'l4', []),
 ('Дах уже не тече. А звідки взялись гроші на гнилі крокви — покаже шоста частина.', 'Дах уже не тече. А звідки взялись гроші на гнилі кро́кви — покаже шоста частина.', 'n1', []),
 ('Щомісяця: оренда — 50 тисяч, мій кредит — 27, кредит Влада — 18. Плюс зарплати, медовуха і світло.', "Щомісяця: оренда — п'ятдесят тисяч, мій кредит — двадцять сім, кредит Влада — вісімнадцять. Плюс зарплати, медовуха і світло.", 'n2', []),
 ('Разом бар витрачає понад 300 тисяч на місяць. А каса в добрий тиждень — 110.', 'Разом бар витрачає понад триста тисяч на місяць. А каса в добрий тиждень — сто десять.', 'n3', []),
 ('Якщо все піде добре, бар окупиться за півтора-два роки. Якщо.', 'Якщо все піде добре, бар окупиться за півтора-два роки. Якщо.', 'n4', []),
 ('А ти б яку з цих помилок не зробив? Пиши в коментарях. І підписуйся — далі шоста частина, «Гість».', 'А ти б яку з цих помилок не зробив? Пиши в коментарях. І підписуйся — далі шоста частина, «Гість».', 'e1', []),
]
SFX = [("s3", "штраф", "stamp"), ("s5", "кредит", "stamp")]
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
