# SmartiHats — website

A static, single-page marketing site for **SmartiHats** — smart-home
installation & support serving Sandy Springs and Metro Atlanta.

- **No frameworks, no build step, no backend.** Plain HTML + CSS + a small
  vanilla-JS file.
- **Mobile-first**, system font stack (zero font downloads).
- **One conversion goal:** request a consultation (via Formspree).
- All colors are WCAG-AA contrast-checked; every check is automated by the
  [dogfood validator](#dogfood-validator-run-after-every-edit).

```
smartihats-site/
├── index.html      # the page (all content lives here)
├── styles.css      # all styling
├── script.js       # form validation + footer year (loaded with defer)
├── dogfood/
│   └── dogfood.py  # validation harness (python3, no dependencies)
└── README.md       # this file
```

This is plain static HTML — you can open `index.html` straight from your
computer, or deploy it to GitHub Pages.

---

## Deploying to GitHub Pages (→ smartihats.com)

### Step 1 — create the repo and push

```bash
# from inside this folder (smartihats-site/)
cd /home/dad/smartihats-site

git init
git add -A
git commit -m "SmartiHats static site"

# replace YOUR_GH_USERNAME with your GitHub handle
git remote add origin git@github.com:YOUR_GH_USERNAME/smartihats.git
git branch -M main
git push -u origin main
```

> Your GitHub handle for this already runs `faceid.smartihats.com`
> (it resolves to `vgerald.github.io`), so `vgerald` is the likely account —
> confirm before pushing.

### Step 2 — enable Pages

1. GitHub → your `smartihats` repo → **Settings → Pages**.
2. **Build and deployment** → Source: **Deploy from a branch** → Branch:
   `main`, folder: `/ (root)` → **Save**.
3. Wait ~1–2 minutes. Your site is now live at
   `https://YOUR_GH_USERNAME.github.io/smartihats/`.

### Step 3 — verify, then claim the custom domain

1. **Check `https://YOUR_GH_USERNAME.github.io/smartihats/` loads correctly
   first.** Only after confirming the site is healthy do you point the real
   domain at it.
2. In the same **Settings → Pages** panel, under **Custom domain**, type
   `www.smartihats.com` and click **Save**. (GitHub will list `smartihats.com`
   as the root — use the `www` subdomain for the CNAME; see DNS below.)

### ⚠ Step 4 — DNS (READ THIS BEFORE YOU TOUCH IT)

**What is true right now** (checked 2026-11-09 via `dig` + `curl`):

| Record | Current value |
|---|---|
| `smartihats.com` (apex) A | `13.248.243.5` + `76.223.105.230` — **GoDaddy Website Builder** (serves *another*, older SmartiHats site) |
| `www.smartihats.com` | CNAME → `smartihats.com` |
| `faceid.smartihats.com` | CNAME → `vgerald.github.io` (GitHub Pages, already working) |
| authoritative nameservers | **GoDaddy** |

**The decision first:** swapping the apex records makes *this* site the
apex and **stops the old GoDaddy Website Builder site from being served at
`smartihats.com`/`www`.** Three options:
(1) **Replace it** — the new site supersedes it (this guide's path);
(2) **Keep both** — host the new one at a subdomain (e.g. `www` → Pages,
apex unchanged) and build it out later;
(3) **Migrate the old site's content into this site** and then replace.
Pick one; option 1 is what the steps below do.

**GoDaddy portal steps (option 1):**

1. **GitHub first:** repo **Settings → Pages** → *Build and deployment*:
   source **Deploy from a branch**, branch `main` (or your default), folder
   **`/ (root)`**. Under *Custom domain* enter **`www.smartihats.com`** →
   **Save**. GitHub auto-adds `smartihats.com` as "root domain" and issues
   HTTPS itself (ENFORCE HTTP→HTTPS should be on).
2. **GoDaddy:** *My Products → DNS* (or search **smartihats.com → DNS**).
3. **Type A (apex):** edit the two existing A records (`13.248.243.5`,
   `76.223.105.230`) — **delete** them, then **Add Record → Type A** four
   times, name left as `@`, values:
   `185.199.108.153` · `185.199.108.154` · `185.199.109.153` · `185.199.110.153`
   (standard ~600 s TTL is fine).
4. **Type CNAME (www):** edit the existing `www` record: value →
   **`vgerald.github.io`** (was `smartihats.com`).
5. Save. GitHub's dashboard will flip the domain from ⏳ to ✅ (can take
   minutes). Propagation is usually < 1 h; **up to 24–48 h** worst case
   (old A records' TTL + CDN caches), so the old site may linger briefly in
   some caches — that's normal, not a failure.
6. Verify: `https://smartihats.com/` and `https://www.smartihats.com/` both
   serve **this** site over valid HTTPS, 301 `www` → apex (or vice versa —
   GitHub normalizes to the apex after both are claimed; we set `www` as
   the CNAME side per GitHub's recommendation, apex via A-records).

> **Face ID service (`faceid.smartihats.com`) is untouched** — GitHub
> custom domains are per-repo, and that CNAME stays on `vgerald.github.io`.

---

## Connecting the Formspree form ✓ (done 2026-11-09)

The form is wired with the **Basic HTML** guide: a plain
`<form action="https://formspree.io/f/mbggvnql" method="POST">` — native
POST, no external JS, no CORS, and it keeps the "zero dependencies" rule
that the dogfood validator enforces (check f2 would fail the CDN
`@formspree/ajax` version). Tailored pieces:

- `_subject` hidden field → inbox emails titled **"SmartiHats — new
  consultation request"**
- `_gotcha` honeypot → bot spam discarded by Formspree
- our own email/phone/ZIP validation runs client-side first (see script.js)
- a diagnostic fallback card is kept in the markup: if the action ever
  reverts to a placeholder ID, visitors still get working phone/email
  links instead of a dead form

Submissions land on the **free "SmartiHats consultation" plan** (50/month)
→ check the reply-to in Formspree's email dashboard and set up forwarding
to where you actually want them. If you create a replacement form later,
change the `<form action>` in `index.html` exactly once and re-run dogfood
(check `c3` verifies the wiring). **The form intentionally does not ask
for any passwords, credentials, or account access** — dogfood check `c5`
hard-fails the build if one is ever added.

---

## Where to replace placeholder content

Everything the dogfood validator flags is listed here with its location.
Search `TODO(` in `index.html` to jump to each one.

| What | Where | Replace with |
|---|---|---|
| ~~**Formspree Form ID**~~ | **done** — `index.html` `<form action>` = `https://formspree.io/f/mbggvnql` (wired 2026-11-09); dogfood check `c3` verifies it | — |
| **Phone number** | Hero contact line, contact panel, footer (search `010-0199`) | your real number |
| **Email address** | Hero contact line, contact panel, footer (search `hello@smartihats.com`) | your real address |
| **Founder intro** | "About & Proof" section — the `<p>` after the "Founded by …" heading | your real bio |
| **Photo grid** | "About & Proof" section — `<div class="grid grid-3">` of `<figure class="photo">` (currently 3 inline-SVG demos: scheduling, cameras, support) | replace each demo's `<svg>` with a real `<img src="photos/…" alt="what a person can't guess from the filename" loading="lazy" width="800" height="600">`; keep the "Demonstration setup" badge on non-client work; **never** present a demo as a client project |
| **Testimonials** | "About & Proof" section — `<div class="testimonials-placeholder">` | your genuine, attributed quotes as they're earned |
| **Legal / privacy** | "No credentials, ever" note in the form area | adjust only if your actual policy changes |

The `© <span id="year">` in the footer fills automatically (no edit needed).

---

## Dogfood validator (run after every edit)

One command, no dependencies (Python 3 stdlib only):

```bash
cd /home/dad/smartihats-site
python3 dogfood/dogfood.py .          # pass a different dir if needed
```

It runs 8 families of checks and **exits 0 only on a full pass** (non-zero if
any fail) — so it's safe to wire into a script or CI:

| # | Check | What it verifies |
|---|---|---|
| a | **HTML validity** | balanced/void tags, no unclosed elements, no duplicate `id`s |
| b | **Links** | internal `#anchors` resolve to real `id`s; external links are `https` |
| c | **Form** | all required fields present, Formspree marker present, **every input labelled**, and a **hard FAIL if any password/credential field exists** |
| d | **Mobile** | `viewport` meta (`width=device-width`) present; no fixed pixel widths / rule-body `min-width` that would cause horizontal scroll |
| e | **Accessibility** | every `<img>` has `alt`, all `role="img"` SVGs labelled, exactly one `h1`, heading levels never skip, text/background contrast ≥ 4.5:1 (WCAG AA) |
| f | **Performance** | total page weight < 1 MB, no render-blocking/remote `<script src>`/CSS, zero external fonts |
| g | **SEO** | `<title>`, meta description, and parseable `LocalBusiness` JSON-LD all present |
| h | **Placeholder audit** | lists every `TODO(…)` marker + known placeholder strings (informational — tells you what content is still missing before launch) |

**Contrast note:** e4 is a *static* approximation (resolves `var()` from
`:root`, checks declared colors against their known containers). It's
conservative, but for final sign-off after your real photos and copy are in,
also run a browser auditor — Lighthouse, axe, or WAVE.

### Adding a check

Open `dogfood/dogfood.py`, find the matching lettered section, and add a
`rep.add("<n> <name>", ok_bool, "human detail on failure")`. A `False`
bumps the exit code and prints `[FAIL]`. Informational (always-pass) lines
use `rep.note(...)`.

---

*Built to be small, fast, honest, and private-by-design. One page, one CTA.*
