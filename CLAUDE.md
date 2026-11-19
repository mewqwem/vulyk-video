# Project context: animated business-story TikTok series

Language with the user: Ukrainian. He prefers step-by-step explanations and targeted fixes over rewrites.

## Goal
Ukrainian-language TikTok channel: short animated vertical videos (1080x1920, ~2 min) telling a multi-part story of
opening a business, with a money counter that keeps dropping, a surprise problem at each step, and a cliffhanger
("пиши в коментарях", next part). Monetisation plan: sell 3–5 s ad integrations inside videos and send viewers to a
Telegram channel (TikTok Creator Rewards is not available in Poland/Ukraine).

## Canon (source of truth) — READ FIRST before writing any part
canon.md holds every fact that must never change (bar, money, loan, rent, shares, people, timeline, balance per part,
open threads, still-undecided items). A new part must not contradict it; only ADD facts to it after each part.
Before voicing/rendering a part run `python3 check_canon.py` (balances chain part to part and match canon.md §6);
when a part is finished, add its row to §6 and update the open threads (§7).

## Current story: bar «Вулик» (fictional — never use real bar brands)
Bar in Lviv that serves only mead (медовуха), bartenders styled as beekeepers, honeycomb bar counter; focus on
atmosphere and service. Start 1 500 000 ₴ (700k loan + 800k savings).
Part 1 is DONE (parts/part1/lines.py): premises → own brewing turns out to be production (excise, licence) → renovation of an
1895 building → neon sign not approved in the historic centre → counter/furniture/equipment → alcohol licence
(~13 000 ₴/yr per cash register, real 2026 figure) → stock + 3 bartenders → blackout: generator + music royalties.
Ends at 35 000 ₴ with rent of 70 000 due; an investor offers 300 000 ₴ but wants beer and cheap shots (kills the concept).
Characters: characters.md — first names only, no surnames. Hero Назар, 29, narrator, ex-senior bartender (his bar
vanished overnight: only a subtle hint at the war, never say it); friend & 50% co-owner Влад, 29, former hall administrator
of the same bar, charismatic negotiator who overspends and overpromises (after part 2 more careful, but not always);
Мілана, 20, chemistry student, the only one of the 3 hired bartenders who shows up on opening day.
Part 2 «Відкриття»: plot draft in parts/part2/plan.md with a DAY counter (part 1 = days 1–30, part 2 = days 31–41,
opening on day 40). The episode's problem is STAFF (2 bartenders ghost after taking salary in advance). Влад invests 400 000;
costs: rent 50k, loan payment 27k, bloggers 45k, logo glasses 24k, stock 60k, one-night bartender 5k; first night only
+31 000 (below the 129k it took to prepare); ends at 255 000; cliffhanger: find new staff or demand the money back?
The user wants money and time to feel believable, not easy. Status 2026-11-11: part 2 video DONE (parts/part2/part2.mp4, 2:41).
Part 2 scene.html = part 1 helpers + its own renderSteps: START/PEAK balance with income (negative ded = green +),
DAY counter in the balance card (DAY map by scene key), heroCard(), VLAD / MILANA / BLOGGERS outfits, W(key,i) = start
time of word i so pops sync to speech. One scene key per line. New part = copy part2 folder as the template.
Part 3 «Команда» DONE 2026-11-13 (parts/part3, days 41–48, 255 000 → 307 500): Taras returns 15k, Denys blocks, lawyer
(no contract, nobody registered, fine up to 86 470 × 3), new rules (official + 22% ЄСВ, accountant 4k, nothing upfront),
hires Оля and Ігор, first week in plus, finale: Nazar lists legal checks before an inspection (open question to viewers,
no two-option choice) → part 4 «Перевірка»; neighbours postponed. Redone 2026-11-13: short text (28 lines), video 2:17. Author wants parts ≤ 2:30 (max ~1 900 chars of text); voice speed 1.1
via VOICE_SPEED in lines.py (voice_lumean.py sends it as config_override; parts 1–2 stay at 1.0). Scenes use WS(key,'wordstart') instead of word indices. Sound effects:
make_sfx.py synthesises sfx/*.wav; build.py mixes cash in/out, whooshes, SFX=[(scene,word,name)] from lines.py, and a pop/stamp
for EVERY element that pops on screen (render.py timing.json --pops → pops.json; scene.html pop() records window.__pops).
Author wants SFX quiet (VOL in build.py lowered 2026-11-13) and a sound on every appearing element.
Keep amounts consistent: the balance card is computed from the deductions in lines.py.

## Pipeline (see README.md)
Each part is a folder parts/<partN>/ with its own lines.py (TITLE + LINES) and scene.html; all generated files land there.
Shared tools take the folder: voice_lumean.py parts/partN, build.py parts/partN. New part = copy the folder, rewrite.
lines.py (script + scene keys + deductions) → voice_lumean.py parts/partN (whole text in ONE order for even intonation, then cut
into lines by word timings; `parts/partN 3,7` redoes single lines as separate orders) → build.py parts/partN (voice mix, render via headless Chromium + ffmpeg, mux; `--voice-only` = just voice.wav).
Run build/render with .venv/bin/python (playwright lives there). Inter font in fonts/, loaded by scene.html.
scene.html holds all drawing: person() character (moods: neutral/happy/sad/worried; options shirt/hair/extra for
other characters like SUIT and APRON), balanceCard, pill, tag, stamp, bubble, props; renderSteps(t) switches on the
scene key of the current line. A new part = new LINES + new cases in renderSteps.
app.py + studio.html = read-only viewer by part (live preview, script with balance, finished videos).
The user works with me in chat; the viewer is only for looking at results, not for editing or running steps.
Before a full render, take stills from inside the part folder: `python ../../render.py timing.json x.mp4 t1,t2,...` and look at them.

## Voice
Chosen provider (2026-11): Lumean (https://lumean.app), a reseller over ElevenLabs/HeyGen/Cartesia. Full API reference:
https://api.lumean.app/docs/llm.md. Base https://api.lumean.app/api/public, header X-API-KEY (key in vulyk-video/.env,
never in chat). Flow: voice_id from GET /voices?provider=elevenlabs → template (POST /templates, service_key elevenlabs,
language_code "uk") → POST /orders {template_id, input_text} → poll GET /orders/{id} → POST /storage/url for each path in
result.files[] (mp3) and result.service_files[] (srt/vtt/lrc, alignment.csv, result.json).
result.json = schema "el-timestamps/v1" with alignment.characters / character_start_times_seconds / ..._end_... —
the same shape as ElevenLabs, so words_from_alignment() works. Orders finish in ~15 s.
Template "Вулик · оповідач" (id in .env as LUMEAN_TEMPLATE_ID): eleven_multilingual_v2, uk, stability .45, similarity .8,
speed 1.0, stability 0.6, prev_next_text on (was 1.08/0.45: user heard speed-ups and a 'different voice'); other voices per order via config_override.tts_settings.voice_id. Account pays from LumCoin balance (no
subscription). Cost is tiny: min 500 billable chars per order ≈ 0.023 LMC; whole part 1 ≈ 0.083 LMC.
2026-11-11 test of the hook: Alex Nekrasov 9Sj8ugvpK1DmcAXyvi3a vs Yaroslava 0ZQZuw8Sn4cU0rN1Tm2K (voice_samples/).
Chosen voice (2026-11-11): Alex Nekrasov – Confident and Clear (9Sj8ugvpK1DmcAXyvi3a), set in the template. Part 1 voiced: 128 s.
ElevenLabs (paid, best quality, gives word timestamps). Free local fallback for Ukrainian: tts_uk / robinhad
ukrainian-tts (check model licence before commercial use). Chatterbox/F5/Fish/XTTS have no Ukrainian; only
Chatterbox is MIT (commercial OK). The `+` marks in the TTS text are stress marks for the offline model; they are
stripped for ElevenLabs.

Character voices (from part 4): lines.py CAST = {name: voice_id} and VOICED_BY = {line index: name}; narrator lines
still go in ONE order, character lines are separate orders. Vlad = Nestor Lipich GVAs5c0aXpTTBsFQ9emv in ENERGETIC mode: settings stability 0.3, style 0.6 (calm default
didn't fit — Vlad is energetic; chosen 2026-11-13). CAST value may be {"voice": id, "settings": {...}}.
A character's quote is its own line (own scene key), the narrator's lead-in stays on the previous line.
Part 5 «Дах» DONE 2026-11-16 autonomously (days 62–74, 190 000 → 298 500, parts/part5/plan.md lists my own decisions). Part 4 «Перевірка» (days 49–62, 307 500 → 190 000): rewritten 2026-11-16 after viewer comment (lawyer checklist, cheap supplier unchecked, courtyard tables → landlord call about the roof), hook opens on the fine; lines.py voiced; video not made yet. Hooks must hit the problem in the first second (viewers drop at 0–1 s).
Recap after part 5 DONE 2026-11-17 (parts/recap1, 1:49, not a canon part: folder name is not partN so check_canon skips it;
its card counts money PUT IN 0 → 2 300 000 and the number of loans instead of balance/day). It says the roof no longer
leaks and part 6 will show where the money for the rafters came from — part 6 must cover that.

## Captions and stress (user feedback 2026-11-11)
Captions are karaoke: a group of up to 3 words, only the word being spoken is orange, the rest white (*word* marks in
captions no longer change colour). Stress: multilingual_v2 ignores `+`; put a combining acute U+0301 after the stressed
vowel in the TTS text (стара́, сті́йка). A full stop instead of a comma gives a pause.

## Publishing (from 2026-11-16)
Telegram via our own bot: `python3 tg_post.py me parts/partN` sends partN.mp4 + post_tg.txt to the author's private chat
with the bot (draft); `channel` posts to «Мінус Мільйон» — ONLY after the author says yes. `ids` lists chat ids.
.env: TG_BOT_TOKEN (never print), TG_ME_CHAT_ID, TG_CHANNEL_ID. Captions per part: post_tg.txt, post_tiktok.txt.
Browser/computer-use can't attach files (file pickers are off-limits) — use the bot. TikTok upload stays manual.
