# Twilio A2P 10DLC — missed-call text-back, as a reseller

Researched and verified against primary sources 2026-07-30 (Twilio docs + IRS). This governs the
text-back tier of the service ladder. **Re-verify fees before quoting a client — they move.**

---

## 1. What you are registering, in plain terms

Since 2021 US carriers require every business sending automated texts from a normal 10-digit number
to be registered. The standard is **A2P 10DLC** (Application-to-Person, 10-Digit Long Code).
Unregistered traffic gets surcharged and increasingly blocked.

Two things get registered, in order:
1. **Brand** — who the sender is. Approves in **minutes**.
2. **Campaign** — what they'll send. **Manual vetting, can take SEVERAL WEEKS.**

⚠️ **The "days per client" figure in older notes was wrong.** Campaign vetting is weeks. Start a
client's registration the day they sign, never the week you launch.

---

## 2. The three brand tiers

| | **Sole Proprietor** | **Low-Volume Standard** | **Standard** |
|---|---|---|---|
| EIN required | **No** | **Yes** | Yes |
| Brand fee | ~$4.50 | **~$4** | ~$44 |
| Campaigns per brand | **1** | up to 5 | up to 5 |
| Phone numbers | **1 (hard limit)** | multiple | multiple |
| Daily volume (T-Mobile) | ~3,000 segments | ~6,000 | higher |
| Use cases | restricted | broader | full |

**Low-Volume Standard costs the same as Sole Proprietor and is far less crippled. The only thing
between them is an EIN.**

⚠️ **Having an EIN DISQUALIFIES you from Sole Proprietor.** It is specifically for people with no
tax ID. So this is not "pick the better tier" — getting an EIN moves you.

### The EIN (verified at irs.gov)
- **Free.** IRS warns explicitly: *"You never have to pay a fee for an EIN."* Any site charging is a scam.
- **A sole proprietor with no LLC can get one.**
- **Issued immediately online**, takes minutes. Needs the responsible party's SSN.
- **Hours** (not 24/7): Mon-Fri 6am-1am ET · Sat 6am-9pm · Sun 6pm-midnight.
- **One EIN per responsible party per day.**

---

## 3. 🔴 THE RESELLER RULE — the one that silently caps the business

> Twilio, verbatim: **"All required information pertains to the business sending the messages, not
> the agency/ISV submitting it."**

**The limit is 10 brands per email address and per physical address, ecosystem-wide** (counts even
against registrations made through other vendors).

That limit attaches to **whoever's email and address are on the registration**:

- ❌ **Your email + your address on every client brand → you hard-cap at 10 clients.**
- ✅ **Each client's own email + own address on their own brand → every client starts fresh. Uncapped.**

**This is silent.** Nothing warns you; client eleven simply fails. Build onboarding around the
client's credentials from day one.

Also: a mobile number can verify at most **3 Sole Proprietor brands**, lifetime, ecosystem-wide.

**Division of labour:** *you* submit, *they* supply. That is the service being charged for.

---

## 4. Client intake — collect ALL of this before starting

| Field | Notes |
|---|---|
| Legal business name | **Must exactly match the EIN registration** if they have one |
| EIN | Or explicit confirmation they have none → Sole Proprietor path |
| Business type / industry | |
| Business street address | **Theirs, never ours** |
| **Business email** | ⚠️ **Free/personal domains get rejected — see §5** |
| **Website URL** | ⚠️ **Required, must be live and match the business name — see §5** |
| Authorized rep | Name, job title, phone (E.164), email |
| Social profile URLs | Helps vetting |
| Two sample messages | Max 1,024 chars each, must include business name + opt-out |
| Opt-in description | How the customer consented |

---

## 5. 🔑 THE SALES ANGLE HIDDEN IN THE REQUIREMENTS

Two registration fields are things our target clients **do not have**:

1. **A business email on a real domain.** TCR rejects free/personal email domains. Our entire
   pipeline is on free gmail: four of the five current clients use a
   personal gmail address rather than a domain mailbox. **Every one would likely fail brand registration.**
2. **A live website whose name matches the business.** Most of our prospects have none.

**We sell both.** A website comes with a domain, a domain gives them `info@example-business.com`.

> **"You can't legally text your customers back without a website and a business email on your own
> domain. I do both, and then I turn the texting on."**

That reframes the website from a nice-to-have into a **prerequisite**, and it is true rather than a
sales device. It is the strongest single argument in the whole ladder — use it.

---

## 6. Unit economics per client

| Item | Cost |
|---|---|
| Brand registration | ~$4 one-time |
| Campaign vetting | ~$15 one-time |
| Campaign monthly | ~$1.50–10/mo |
| Phone number | ~$1.15/mo |
| Per SMS | ~$0.008 + ~$0.003–0.005 carrier surcharge |

**≈ $19 to onboard, then $3–12/mo** at typical missed-call volume. Against a $99–$499/mo tier that
is **1–12% of revenue**. Twilio bills OUR account for all of it; it is marked up into their monthly.
**Cost was never the constraint — the weeks-long campaign vetting is.**

---

## 7. Missed-call text-back: the consent basis

The customer **called them first**. The inbound call is the consent basis for an automated reply to
that number, and it is why this use case is defensible where cold texting is not.

Regardless, every first message must carry: **business name · what this is · how to stop.**

⚠️ **TCPA is a genuine litigation area and I am not a lawyer.** Never promise a client legal
compliance. Ship the opt-out on message one, keep the consent basis documented in the campaign
description, and tell them to run it past their own counsel if they are worried.

---

## 8. Alternative: toll-free verification

Toll-free numbers use a **separate, usually faster** verification path and skip 10DLC entirely.
Trade-off: a toll-free number reads less local, which matters for a the exurban county trade whose whole
pitch is "local guy." **Worth pricing if multi-week campaign vetting becomes the bottleneck.**
Not yet verified in depth — do that before recommending it to a client.

---

## Sources
- Twilio: [A2P 10DLC overview](https://www.twilio.com/docs/messaging/compliance/a2p-10dlc) ·
  [Direct Sole Proprietor](https://www.twilio.com/docs/messaging/compliance/a2p-10dlc/direct-sole-proprietor-registration-overview) ·
  [Collect business info](https://www.twilio.com/docs/messaging/compliance/a2p-10dlc/collect-business-info)
- IRS: [Get an EIN](https://www.irs.gov/businesses/small-businesses-self-employed/get-an-employer-identification-number)
