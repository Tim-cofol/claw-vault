import json, re, sys

def body(path, marker=None, maxlen=2200):
    d = json.load(open(path))
    for r in d.get("results", []):
        t = r.get("raw_content", "") or ""
        print("##### URL:", r.get("url"))
        i = 0
        if marker:
            j = t.find(marker)
            if j < 0:
                print("[marker not found]", marker)
            else:
                i = j
        print(t[i:i+maxlen])
        print()

for p in sys.argv[1:]:
    path, _, marker = p.partition("::")
    body(path, marker or None)
