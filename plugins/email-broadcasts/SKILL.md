---
name: email-broadcasts
description: >
  Draft, test, and send marketing / product-update email broadcasts to an audience via Resend.
  Use when the user asks to "send a broadcast", "email blast", "newsletter", "product update
  email", "announce something to users", "marketing email", "review request", "how many
  contacts", "email history", or "what have we sent". Config-driven brand + sender; mandatory
  test send and explicit confirmation before any real send; CAN-SPAM compliant; bounded history.
---

# Email Broadcasts

<objective>
Manage product-update and marketing email broadcasts via Resend Broadcasts. Covers the full
workflow: audience sync/count, drafting (per design rules), a **mandatory test-send preview**,
an explicit user confirmation gate, sending to your audience, and history tracking with
rolling-window pruning. CAN-SPAM compliant. You set your brand, sender, addresses, and
segment IDs in `references/config.md`. NEVER sends to the full audience without an explicit
confirmation phrase ("yes send it").
</objective>

<context>
@references/config.md
@history.md
</context>

<execution_context>
- 🟢 Auto: contact/audience counts, history reads, knowledge lookups
- 🟡 ASK on: draft generation (preview required), test-segment send (still asks before the real send)
- 🔴 NEVER: send to the general audience without an explicit "yes send it" (or "schedule it for X")
- Mandatory self-preview: ALWAYS send a test broadcast to the test segment first, wait for "looks good"
- History: keep the last 5 broadcasts full, archive older to one-line at the bottom of `history.md`
</execution_context>

## Setup (one time)

Fill in `references/config.md` (brand, from/reply-to, physical address for CAN-SPAM, audience
+ test segment IDs, test recipients). Set:

```bash
export RESEND_API_KEY="your-key"   # free key at https://resend.com
```

Manage contacts in your Resend **Audience** (import a CSV, or sync from your own source). This
skill treats the Resend audience as the source of truth — no specific backend is assumed.

## Routing — what does the user want?

| User says | Route to |
|-----------|----------|
| "send/draft a broadcast", "announce", "newsletter" | → **Draft & Send workflow** |
| "how many contacts/subscribers" | → **Resend: list contacts / audience count** |
| "what have we sent", "email history" | → **History** |
| "open rate", "stats" | → **Resend: list/get broadcast** |
| "how does unsubscribe / CAN-SPAM work" | → **Knowledge lookup** (below) |

## Draft & Send Workflow

### Phase 1 — Prepare
1. Confirm the audience + count (Resend `list-contacts` / audience).
2. Ask: purpose (product update, announcement, review request, custom)? What to highlight? CTA?

### Phase 2 — Draft
Compose the email (HTML + plain text). Proven structure:
```
Short, warm intro (2-3 sentences)
WHAT'S NEW — section header + one card per item
A SMALL ASK — the CTA + a short line of context
Sign-off + footer + unsubscribe
```
**Subject lines:** short (<40 chars), friendly, no "review/survey", no ALL CAPS, no emoji.

**HTML rules:** table-based layout; all styles inline (no `<style>` tag); 600px max width;
`bgcolor` alongside CSS for Outlook; no JS, no background images; keep it text-heavy on early
sends for deliverability; always include a plain-text version.

### Phase 3 — Test (MANDATORY)
**Never skip. Never send without explicit confirmation.**
1. Create a broadcast on the **test segment** (id from config).
2. Send the test (only goes to your test recipients).
3. Ask the user to check: inbox placement (not Promotions/Spam), rendering, CTA target, the
   unsubscribe link, mobile, and the from-name.
4. Wait for explicit approval: **"yes send it"** or **"schedule it for X"**.

### Phase 4 — Send
Only after explicit confirmation:
1. Create the broadcast on the **general audience/segment** (id from config).
2. Send or schedule via Resend.
3. Record it in `history.md`.

### Phase 5 — Clean up
Update `history.md` (keep last 5 full, older → one-line). Verify delivery via Resend
`list-broadcasts` / `get-broadcast`.

## CAN-SPAM Compliance

Every marketing email MUST include:
- A physical mailing address (from config).
- A working unsubscribe link (Resend Broadcasts auto-manage this; it injects a
  `List-Unsubscribe` header and skips unsubscribed contacts on future sends).
- An honest subject line, no deception.
- A real reply-to / support contact (from config).

## Tools — when to use what

| Task | Tool |
|------|------|
| List/manage contacts | Resend MCP/API (`list-contacts`, `create-contact`, `update-contact`) |
| Create/send broadcast | Resend MCP/API (`create-broadcast`, `send-broadcast`) |
| One-off transactional email | Resend MCP/API (`send-email`) |
| Check broadcast stats | Resend MCP/API (`list-broadcasts`, `get-broadcast`) |

## History

`history.md` format per entry:
```
## [Date] — [Subject]
- Recipients: [N]
- Segment: General / Test
- Status: sent / scheduled [date]
- Key content: [1-line summary]
```
Keep the last 5 full entries; older → one-line archive at the bottom.

<saved_rules_format>
Stored in `history.md` "Saved Rules" section, surfaced each run as:
> "Previous rule found: '<rule>'. Apply? (Yes / No / Delete)"
Common topics: subject-line preferences, CTA copy, do-not-send-to-X rules.
</saved_rules_format>

<recovery_protocol>
If `history.md` shows `status: scheduled` for a broadcast that should have sent → verify in the
Resend dashboard. If a draft was interrupted mid-workflow → offer Resume from last phase / Start
fresh / Review.
</recovery_protocol>

<error_handling>
- Resend rate limit → sleep and retry; respect the free-tier limit.
- Test send doesn't arrive → wait, then check; if still missing, stop (don't proceed to the general send).
- Ambiguous approval phrase → re-ask explicitly: "Confirm: send to [N] contacts? Reply 'yes send it'."
</error_handling>

<success_criteria>
- [ ] Audience count verified before the broadcast
- [ ] Test broadcast sent to the test segment FIRST
- [ ] User confirmed the test looked good
- [ ] Explicit "yes send it" (or "schedule it for X") before the general send
- [ ] history.md updated; last 5 full, older compacted
- [ ] Delivery verified after send
