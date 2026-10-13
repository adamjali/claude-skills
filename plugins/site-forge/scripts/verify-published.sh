#!/bin/bash
# Prove on the LIVE host that nothing private is reachable. Run after EVERY deploy.
# Local checks prove nothing: the leak that started this was invisible on disk.
HOST="${1:?usage: verify-published.sh <<client>.netlify.app> [owner-street-name]}"
STREET="$2"
PATHS=(/research/BRIEF.md /research/ /RESEARCH.md /NOTES.md /STATE.md /README.md
       /build.py /pages.py /optimize.py /skin.py /make_map.py /tracker.py /generate.py
       /ogcard.html /package.json /package-lock.json /.env /.git/config /.git/HEAD
       /assets/stock/ /ledger/ /vo.txt /CLAUDE.md)
fail=0
for p in "${PATHS[@]}"; do
  code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 8 "https://$HOST$p")
  if [ "$code" = "200" ]; then echo "  LEAK  $p"; fail=1; fi
done
if [ -n "$STREET" ]; then
  n=$(curl -s "https://$HOST/" "https://$HOST/about/" | grep -ic "$STREET")
  [ "$n" != "0" ] && { echo "  LEAK  owner street name appears $n time(s)"; fail=1; }
fi
[ "$fail" = "0" ] && echo "  clean: nothing private is reachable on $HOST"
exit $fail
