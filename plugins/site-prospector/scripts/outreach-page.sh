#!/usr/bin/env bash
set -euo pipefail
# Generate a copy-pastable outreach drafts page: FB DM -> email -> text,
# sequenced + cross-referenced, with Copy buttons and one follow-up.
# Drafts ONLY — never sent. Writes outside any deploy dir (these are private).
#
# Usage:
#   outreach-page.sh "Business Name" "https://<client>.netlify.app" \
#     "their@example-business.com" "<phone>" "their domain is parked" [outfile]

BIZ="${1:?business name required}"
URL="${2:?site url required}"
EMAIL="${3:-their email}"
PHONE="${4:-their phone}"
HOOK="${5:-they have no website yet}"
SLUG="$(printf '%s' "$BIZ" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9' '-' | sed 's/^-//;s/-$//')"
OUT="${6:-$HOME/Desktop/outreach-$SLUG.html}"
DISPLAYURL="${URL#http://}"; DISPLAYURL="${DISPLAYURL#https://}"; DISPLAYURL="${DISPLAYURL%/}"

cat > "$OUT" <<HTMLEOF
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>$BIZ — Outreach Drafts</title>
<style>
  body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;max-width:720px;margin:40px auto;padding:0 20px;color:#1a1a1a;line-height:1.5;background:#fafafa}
  h1{font-size:1.5rem;margin:0 0 4px}.sub{color:#666;margin:0 0 24px;font-size:.95rem}
  .strategy,.draft,.followup{background:#fff;border:1px solid #e5e5e5;border-radius:12px;padding:18px;margin-bottom:20px;font-size:.93rem}
  .fill{background:#fff7ed;border:1px solid #fed7aa;border-radius:8px;padding:10px 14px;margin:14px 0 24px;font-size:.88rem;color:#9a3412}
  .badge{background:#1a1a1a;color:#fff;font-size:.78rem;font-weight:700;width:24px;height:24px;border-radius:50%;display:inline-grid;place-items:center;margin-right:8px;vertical-align:middle}
  .field{font-size:.74rem;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:#888;margin:12px 0 4px}
  pre{background:#f6f6f6;border:1px solid #e8e8e8;border-radius:8px;padding:14px 16px;white-space:pre-wrap;word-wrap:break-word;font-family:inherit;font-size:.95rem;margin:0}
  .copy{margin-top:10px;background:#2563eb;color:#fff;border:none;border-radius:7px;padding:8px 16px;font-size:.88rem;font-weight:600;cursor:pointer}.copy.done{background:#16a34a}
</style></head><body>
<h1>$BIZ — Outreach Drafts</h1>
<p class="sub">$DISPLAYURL</p>
<div class="strategy"><b>Order:</b> 1) Facebook DM first · 2) Email same day/next (references the DM) · 3) Text 2–3 days later <i>only if no reply</i> (references both). Best times early AM / evening, Tue–Thu. One follow-up after that, then stop.</div>
<div class="fill">⚠️ Fill in <b>[your name]</b>, <b>[your phone]</b>, and <b>[your email]</b> before sending.</div>

<div class="draft"><div class="field"><span class="badge">1</span>Facebook DM — send first</div>
<pre id="d1">Hi! I'm [your name] — I build websites for local businesses. I looked up $BIZ and noticed $HOOK, so I figured I'd just build you a new site and show you:

$DISPLAYURL

Modern + mobile, with your story and a simple contact form. No catch, made it as a demo. If you'd want it as your real site (your domain, your email, any tweaks), I'd love to help. Either way, hope it gives you a few ideas!</pre>
<button class="copy" data-target="d1">Copy message</button></div>

<div class="draft"><div class="field"><span class="badge">2</span>Email — to $EMAIL (same day / next)</div>
<div class="field">Subject</div><pre id="s2">Built $BIZ a new website</pre><button class="copy" data-target="s2">Copy subject</button>
<div class="field">Body</div>
<pre id="d2">Hi,

I'm [your name] — I build websites for local businesses. (I also sent you a quick message on Facebook, so this doesn't get buried.)

I looked up $BIZ and noticed $HOOK, so instead of just emailing about it, I went ahead and built you a new one to show you:

$DISPLAYURL

It's modern and mobile-friendly — your story, your work, and a contact form that sends leads straight to your inbox. No catch — I made it as a demo to show what's possible. If you like it, I'd love to make it truly yours (your own domain, your email, any changes). If not, no worries at all.

Take a look and let me know what you think — happy to hop on a quick call too.

[your name]
[your phone] · [your email]</pre>
<button class="copy" data-target="d2">Copy body</button></div>

<div class="draft"><div class="field"><span class="badge">3</span>Text — to $PHONE (2–3 days later, only if no reply)</div>
<pre id="d3">Hi, this is [your name] — I build websites for local businesses. I sent you a Facebook message and an email earlier; just didn't want it to get buried. Short version: $HOOK, so I built $BIZ a new site to show you → $DISPLAYURL. No catch, just a demo — if you like it I'd love to make it yours. Take a look & lmk!</pre>
<button class="copy" data-target="d3">Copy message</button></div>

<div class="followup"><b>One follow-up</b> (3–4 days after the text, if still nothing — then stop):<br><br>"No pressure at all — just circling back once. The site's live here if you get a sec: $DISPLAYURL. Even if you only want it as a free upgrade, it's yours. Either way, take care!"</div>

<script>
document.querySelectorAll('.copy').forEach(function(btn){
  btn.addEventListener('click', async function(){
    var text = document.getElementById(btn.dataset.target).textContent;
    try { await navigator.clipboard.writeText(text); var o = btn.textContent; btn.textContent = 'Copied ✓'; btn.classList.add('done'); setTimeout(function(){ btn.textContent = o; btn.classList.remove('done'); }, 1500); }
    catch (e) { alert('Copy failed — select the text and copy manually.'); }
  });
});
</script></body></html>
HTMLEOF

echo "Wrote outreach drafts: $OUT"
command -v open >/dev/null 2>&1 && open "$OUT" 2>/dev/null || true
