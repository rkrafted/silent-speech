#!/usr/bin/env bash
# Wait out a Google Patents 503 throttle, then fetch every candidate serially.
# Raw HTML goes to research/jaw/raw/ (gitignored).
set -u
cd "$(dirname "$0")/.."
list=research/jaw/patent_candidates.txt
for i in $(seq 1 40); do
  if python3 scripts/fetch_patent.py US10621973B1 >/tmp/probe.out 2>&1; then
    echo "google patents reachable after $i tries"
    break
  fi
  echo "try $i: $(cat /tmp/probe.out)"
  sleep 30
done
# fetch everything, skip already cached
while read -r no; do
  [ -z "$no" ] && continue
  python3 scripts/fetch_patent.py "$no"
  sleep 6
done < "$list"
echo "DONE fetching"
