#!/usr/bin/env bash
set -u
cd "$(dirname "$0")/.."
while read -r no; do
  [ -z "$no" ] && continue
  python3 scripts/fetch_lens.py "$no"
  sleep 1.2
done < research/jaw/patent_candidates.txt
echo LENS_DONE
