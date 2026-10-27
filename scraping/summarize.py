import re, glob, json, statistics as st
out = {}
for f in sorted(glob.glob("ab*_*.txt")):
    L = open(f, encoding="utf-8").read().split("\n"); nights = None; rows = []
    for i, l in enumerate(L):
        m = re.match(r"\$ ([\d.]+) USD por (\d+) noches?$", l)
        if m:
            nights = int(m[2]); price = int(m[1].replace(".", ""))
            blk = L[max(0, i-25):i]
            bd = next((int(re.match(r"(\d+) dormitorio", b)[1]) for b in reversed(blk) if re.match(r"\d+ dormitorio", b)), None)
            rows.append((price, int(m[2]), bd))
    if rows:
        p = [r[0]/r[1] for r in rows]
        out[f[:-4]] = dict(n=len(rows), min=round(min(p)), med=round(st.median(p)), max=round(max(p)), p25=round(st.quantiles(p, n=4)[0]) if len(p) > 3 else None, rows=rows)
        print(f, {k: v for k, v in out[f[:-4]].items() if k != "rows"})
json.dump(out, open("airbnb_summary.json", "w"))
