#!/bin/bash
# EDN 2026-11-11 batch: security vendors + cross-vendor domains
R=/tmp/edn-east/raw
mkdir -p "$R"
run() {
  slug="$1"; flags="$2"; q="$3"
  tvly search "$q" $flags --max-results 15 --json > "$R/$slug.json" 2>"$R/$slug.err"
  n=$(python3 -c "
import json
try:
    d=json.load(open('$R/$slug.json'))
    print(len(d.get('results',[])))
except Exception as e:
    print('ERR:'+str(e)[:40])" 2>/dev/null)
  echo "$slug | $n | $q"
}

PIDS=()
while IFS='|' read -r slug flags q; do
  [ -z "$slug" ] && continue
  run "$slug" "$flags" "$q" &
  PIDS+=($!)
  if [ ${#PIDS[@]} -ge 6 ]; then wait "${PIDS[0]}"; PIDS=("${PIDS[@]:1}"); fi
done < /tmp/edn-east/queries.txt
wait
echo "BATCH DONE"
