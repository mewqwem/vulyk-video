"""Checks the money in every part against canon.md.   Usage: python3 check_canon.py

- part N starts with exactly the balance part N-1 ended with
- each part's start/end matches the table «Баланс по частинах» in canon.md
- every part has a row in that table (add one when a new part is written)
"""
import importlib.util, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def fmt(n):
    return f"{n:,}".replace(",", " ")


def canon_table():
    txt = open(os.path.join(HERE, "canon.md"), encoding="utf-8").read()
    sec = txt.split("## 6.", 1)[1].split("\n## ", 1)[0]
    rows = {}
    for m in re.finditer(r"^\|\s*(\d+)\s*\|\s*([\d\s ]+?)\s*\|\s*([\d\s ]+?)\s*\|", sec, re.M):
        num = lambda s: int(re.sub(r"\D", "", s))
        rows[int(m.group(1))] = (num(m.group(2)), num(m.group(3)))
    return rows


def parts():
    out = []
    for d in os.listdir(os.path.join(HERE, "parts")):
        m = re.fullmatch(r"part(\d+)", d)
        p = os.path.join(HERE, "parts", d, "lines.py")
        if m and os.path.exists(p):
            spec = importlib.util.spec_from_file_location(f"lines_{d}", p)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            out.append((int(m.group(1)), mod))
    return sorted(out, key=lambda x: x[0])


def main():
    table, errors, prev_end = canon_table(), [], None
    for n, mod in parts():
        if not hasattr(mod, "START"):
            errors.append(f"частина {n}: у lines.py немає START")
            continue
        start = mod.START
        end = start - sum(a for line in mod.LINES for _f, a in line[3])
        print(f"частина {n}: {fmt(start)} → {fmt(end)}")
        if prev_end is not None and start != prev_end:
            errors.append(f"частина {n} стартує з {fmt(start)}, а частина {n - 1} закінчилась на {fmt(prev_end)}")
        if n not in table:
            errors.append(f"частини {n} немає в canon.md (розділ 6) — додай рядок | {n} | {fmt(start)} | {fmt(end)} |")
        else:
            cs, ce = table[n]
            if (cs, ce) != (start, end):
                errors.append(f"частина {n}: у lines.py {fmt(start)} → {fmt(end)}, а в каноні {fmt(cs)} → {fmt(ce)}")
        prev_end = end
    if errors:
        print("\n❌ ДІРИ В СЮЖЕТІ:\n- " + "\n- ".join(errors))
        sys.exit(1)
    print("\n✅ гроші між частинами сходяться з каноном")


if __name__ == "__main__":
    main()
