import json, re, requests, pathlib, statistics
root = pathlib.Path(__file__).resolve().parent.parent
S = {}; DATES = {"rio": ("2027-04-01", "2027-04-05"), "arr": ("2027-04-05", "2027-04-07"), "buz": ("2027-04-07", "2027-04-09")}
H = {"User-Agent": "Mozilla/5.0"}
for stop in ("rio", "arr", "buz"):
    S[stop] = {}
    for n in (4, 8, 12):
        rows = []
        for c in json.load(open(root/"scraping"/f"L_{stop}_{n}.json", encoding="utf-8")):
            t = c["text"].replace("\xa0", " "); m = re.search(r"\$ ([\d.]+) USD por (\d+) noches?", t); id_ = re.search(r"/rooms/(\d+)", c["href"] or "")
            if not (m and id_ and c["imgs"]): continue
            lines = [l.strip() for l in t.split("\n") if l.strip()]
            i = next(k for k, l in enumerate(lines) if l.startswith("Foto 1"))
            body = [l for l in lines[i+1:] if not l.startswith(("Favorito", "Superanfitri", "Calificaci", "Foto ", "Nuevo")) and not re.match(r"^[\d,]+ \(\d+\)$", l)]
            rt = re.search(r"([\d,]+) \((\d+)\)", t); bd = re.search(r"(\d+) dormitorio", t); beds = re.search(r"(\d+) cama", t); ba = re.search(r"(\d+) ba", t)
            rows.append(dict(id=id_[1], type=body[0], name=body[1] if len(body) > 1 and not re.match(r"\d+ dorm", body[1]) else "", bd=int(bd[1]) if bd else None,
                beds=int(beds[1]) if beds else None, baths=int(ba[1]) if ba else None, rating=float(rt[1].replace(",", ".")) if rt else None, reviews=int(rt[2]) if rt else 0,
                total=int(m[1].replace(".", "")), nights=int(m[2]), img=c["imgs"][0], free_cancel="Cancelaci" in t))
        uniq = {r["id"]: r for r in rows}.values()
        good = sorted([r for r in uniq if (r["rating"] or 0) >= 4.5 and r["reviews"] >= 5], key=lambda r: r["total"]) or sorted(uniq, key=lambda r: r["total"])
        k = min(6, len(good)); pick = [good[round(i*(len(good)-1)/max(k-1, 1))] for i in range(k)]
        pick = list({r["id"]: r for r in pick}.values())
        for r in pick:
            ci, co = DATES[stop]; r["url"] = f"https://www.airbnb.com.ar/rooms/{r['id']}?adults={n}&check_in={ci}&check_out={co}"
            fn = f"{stop}_{n}_{r['id']}.jpg"; p = root/"assets"/"stays"/fn
            if not p.exists(): p.write_bytes(requests.get(r["img"], headers=H, timeout=30).content)
            r["photo"] = f"assets/stays/{fn}"; r.pop("img")
        S[stop][n] = pick
        print(stop, n, len(rows), "->", [(r["total"]//r["nights"], r["bd"], r["rating"]) for r in pick])
json.dump(S, open(root/"stays.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
