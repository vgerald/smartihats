"""Build pricing hub + 2 tiers + book (consultation form) + 3 support sub + support hub."""
import sys, os
sys.path.insert(0, "/home/dad/smartihats-site")
from gen_helpers import head, footer, book_form

ROOT = "/home/dad/smartihats-site"
def write(rel, content):
    p = os.path.join(ROOT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(content); print("wrote", rel, len(content))

def band(base):
    return ('<section class="block"><div class="wrap"><div class="cta-band">'
            '<h2>Not sure which tier fits?</h2><p>Tell us about your home and we&rsquo;ll map it. No obligation, no pressure.</p>'
            f'<div class="hero-ctas"><a class="btn btn-primary" href="{base}book/">Book a free consultation</a></div></div></div></section>')

def crumbs(base, sec, page):
    return (f'<nav class="crumbs" aria-label="Breadcrumb"><a href="{base}">Home</a> &rsaquo; '
            f'<a href="{base}{sec}/">{sec.capitalize()}</a> &rsaquo; {page}</nav>')

# ================= PRICING HUB =================
body = '<section class="page-hero"><div class="wrap"><span class="kicker">Pricing</span><h1>Three ways to get started</h1><p>Every tier is flat, all-inclusive, and ends with the same outcome: a smart home you own, in one app, with a local expert who answers when you call.</p></div></section>'
body += '<section class="block"><div class="wrap"><h2>Three tiers, one standard</h2><div class="grid grid-3">'
cards = [("add-on", "Add-On", "Perfect starting point", "Single-feature installs that fit in a day or two.", "1,495"),
         ("whole-home", "Whole-Home", "The full build", "Design, install, and configure a complete smart home from scratch.", "6,950"),
         ("residency", "Residency Plan", "Keep it running", "Ongoing support and maintenance that scales with the size of your install. <strong>Monthly.</strong>", "79")]
for slug, t, tag, desc, sub in cards:
    body += (f'<article class="card"><span class="card-tag">{tag}</span><h3>{t}</h3><p>{desc}</p>'
             f'<p class="price-from">From <strong>${sub}</strong></p>'
             f'<p><a class="card-link" href="{slug}/">{t} details &rarr;</a></p></article>')
body += '</div></div></section>'
body += '<section class="block tight"><div class="wrap"><div class="prose">'
body += '<h2>Honest about what&rsquo;s not included</h2>'
body += '<p>Hardware pricing varies with the device counts and brands you choose. We scope that <em>before</em> we send the proposal &mdash; so the number you see is the number you pay. No &ldquo;starting at&rdquo;, no &ldquo;from&rdquo;, no ranges with asterisks.</p>'
body += '<p>If you need a custom quote that doesn&rsquo;t fit a tier &mdash; a partial install, a specific feature list, a phased rollout &mdash; book a consultation and we&rsquo;ll scope it to exactly what you want.</p>'
body += '</div></div></section>' + band("../")
write("pricing/index.html",
      head("Pricing — three tiers, flat, all-inclusive",
           "Smart home pricing for Metro Atlanta: Add-On, Whole-Home, and Residency Plan — flat, all-inclusive, fixed-scope.",
           base="../", active="pricing") + body + footer(base="../"))

# ================= ADD-ON =================
b = crumbs("../", "pricing", "Add-On")
b += '<section class="page-hero"><div class="wrap"><span class="kicker">Pricing · Tier</span><h1>Add-On</h1><p>The perfect starting point. A focused install of one or two features that fits in a day or two.</p></div></section>'
b += '<section class="block"><div class="wrap"><div class="price-card">'
b += '<div class="price-value"><span class="price-from">From</span><strong>$1,495</strong><span class="price-unit">per feature install</span></div>'
b += '<ul class="price-features">'
for f in ["One focused install (camera, lock, thermostat, or a lighting zone)",
          "Proper power and network placement, documented",
          "Commissioned into the unified SmartiHats app",
          "On-site walkthrough and day-one handoff",
          "30-day follow-up and a written config summary"]:
    b += f'<li>✓ {f}</li>'
b += '</ul></div></div></section>'
b += '<section class="block tight"><div class="wrap"><div class="prose">'
b += '<h2>What &ldquo;add-on&rdquo; really means</h2>'
b += '<p>You get a single, focused install &mdash; the thing you&rsquo;ve wanted for a while but don&rsquo;t want a whole renovation to get. The install arrives with the same documentation and day-one handoff as a full build.</p>'
b += '<p>Most add-on installs are scoped in a 20-minute call and scheduled within the week.</p>'
b += '</div></div></section>'
b += '<section class="block"><div class="wrap">' + book_form("../../book/") + '</div></div></section>'
write("pricing/add-on/index.html",
      head("Add-On Pricing", "From $1,495 — one focused smart-home install, properly powered, documented, and commissioned into the unified app.",
           base="../../") + b + footer(base="../../"))

# ================= WHOLE HOME =================
b = crumbs("../", "pricing", "Whole-Home")
b += '<section class="page-hero"><div class="wrap"><span class="kicker">Pricing · Tier</span><h1>Whole-Home</h1><p>Design, install, and configure a complete smart home &mdash; one app, one platform, one accountable owner.</p></div></section>'
b += '<section class="block"><div class="wrap"><div class="price-card">'
b += '<div class="price-value"><span class="price-from">From</span><strong>$6,950</strong><span class="price-unit">for a 3-bedroom home with core devices</span></div>'
b += '<ul class="price-features">'
for f in ["Full design consultation on-site",
          "Wiring, power, and network backbone sized to your device count",
          "Cameras, locks, thermostat, lighting zones, and scenes",
          "Local AI setup (face recognition on the doorbell, anomaly watch)",
          "24/7 local storage sized for your retention window",
          "3-day commissioning and day-one handoff",
          "6-month follow-up and one on-site visit included"]:
    b += f'<li>✓ {f}</li>'
b += '</ul></div></div></section>'
b += '<section class="block tight"><div class="wrap"><div class="prose">'
b += '<h2>How we scope a whole-home</h2>'
b += '<p>We walk the house, map the rooms, and price the device count you&rsquo;ll actually use. Because the square footage and the room count are both known, the install price is a fixed number &mdash; not a range. You&rsquo;ll see the full device list and the full labor list before you say yes.</p>'
b += '<p>We work with the builder for pre-frame installs, and we can retrofit into existing homes when the timing isn&rsquo;t right for a new build.</p>'
b += '</div></div></section>'
b += '<section class="block"><div class="wrap">' + book_form("../../book/") + '</div></div></section>'
write("pricing/whole-home/index.html",
      head("Whole-Home Pricing", "From $6,950 — design, install, and configure a complete smart home with local AI, 24/7 local storage, and a day-one handoff.",
           base="../../") + b + footer(base="../../"))

# ================= RESIDENCY =================
b = crumbs("../", "pricing", "Residency Plan")
b += '<section class="page-hero"><div class="wrap"><span class="kicker">Pricing · Tier</span><h1>Residency Plan</h1><p>Keep it running. Ongoing support and maintenance that scales with the size of your install.</p></div></section>'
b += '<section class="block"><div class="wrap"><div class="price-card">'
b += '<div class="price-value"><span class="price-from">From</span><strong>$79</strong><span class="price-unit">per month</span></div>'
b += '<ul class="price-features">'
for f in ["One number that answers",
          "24/7/365 monitoring for your install",
          "Firmware and security patch watch",
          "Two on-site visits per year (more available)",
          "Unlimited chat and remote diagnostics",
          "Local on-call within 24 hours",
          "Quarterly health report"]:
    b += f'<li>✓ {f}</li>'
b += '</ul></div></div></section>'
b += '<section class="block tight"><div class="wrap"><div class="prose">'
b += '<h2>What &ldquo;residency&rdquo; covers</h2>'
b += '<p>Monitoring for your install, patch watch on the local stack, on-site visits when something needs a pair of hands, and a single number that answers &mdash; a person, not a queue. The plan scales with the size of your install: a full home gets more coverage than a single add-on, and you&rsquo;ll see the difference in the scope sheet we send you.</p>'
b += '<p>You&rsquo;ll always hold the admin key. Support is a relationship, not a lock &mdash; if you ever cancel, your system keeps working.</p>'
b += '</div></div></section>'
b += '<section class="block"><div class="wrap">' + book_form("../../book/") + '</div></div></section>'
write("pricing/residency/index.html",
      head("Residency Plan Pricing", "From $79/mo — ongoing monitoring, patch watch, on-site visits, and one number that answers.",
           base="../../") + b + footer(base="../../"))

# ================= BOOK (CONSULTATION FORM) =================
body = '<section class="page-hero"><div class="wrap"><span class="kicker">Book</span><h1>Book a free on-site consultation</h1><p>No obligation, no pressure, no retainer to start. We walk the space, map the devices, and hand you a clear, fixed-scope proposal.</p></div></section>'
body += '<section class="block"><div class="wrap"><div class="form-wrap">' + book_form("../book/", form_id="consultation") + '</div></div></section>'
write("book/index.html",
      head("Book a free consultation", "Book a free on-site smart-home consultation in Metro Atlanta. Walk the space, map the devices, get a fixed-scope proposal.",
           base="../") + body + footer(base="../"))

# ================= SUPPORT HUB =================
items = [
    ("faq", "FAQ", "Everything about the install process, ownership, support tiers, and what your data looks like after a SmartiHats home."),
    ("service-area", "Service Area", "Sandy Springs and Metro Atlanta. Here&rsquo;s the coverage map and what&rsquo;s on-site and what&rsquo;s remote."),
    ("contact", "Contact", "Phone, email, and a direct line for existing customers. We answer &mdash; no menu, no queue."),
]
body = '<section class="page-hero"><div class="wrap"><span class="kicker">Support</span><h1>How we help after install</h1><p>Support isn&rsquo;t a ticketing system. It&rsquo;s a relationship with a name and a local zip code &mdash; and here&rsquo;s how we keep it working for you.</p></div></section>'
body += '<section class="block"><div class="wrap"><h2>Three ways to reach us</h2><div class="grid grid-3">'
for slug, t, d in items:
    body += f'<article class="card"><h3>{t}</h3><p>{d}</p><p><a class="card-link" href="{slug}/">{t} &rarr;</a></p></article>'
body += '</div></div></section>'
body += '<section class="block tight"><div class="wrap"><div class="prose"><h2>What we don&rsquo;t do</h2><p>We don&rsquo;t sell you a contract you can&rsquo;t read. We don&rsquo;t hold your system hostage after the warranty lingers. If you ever need to leave &mdash; you keep the system, the credentials, and the data. The relationship is the point, not a lock.</p></div></div></section>'
body += band("../")
write("support/index.html",
      head("Support — how we help after install",
           "Smart home support in Metro Atlanta: FAQ, service area, and one number that answers. No ticketing maze.",
           base="../", active="support") + body + footer(base="../"))

# ================= FAQ =================
b = crumbs("../", "support", "FAQ")
faq = [
    ("What does the install actually take?", "Most add-ons are a day or two. Whole-home installs are scoped to your square footage and device count, typically two to three weeks with a hard stop on your calendar. We send the timeline before we start."),
    ("Who keeps the admin key?", "You do. Day one. We hold it for maintenance while you&rsquo;re on the residency plan, but you always have access and you can revoke ours anytime."),
    ("What happens when the internet is down?", "Local cameras keep recording, local AI keeps running, and scenes that don&rsquo;t need the cloud keep working. Remote access pauses &mdash; that part requires the tunnel &mdash; but the home still runs for the people in it."),
    ("Do I have to use your brand of cameras, locks, and thermostats?", "No. We work with the major brands you&rsquo;re already comfortable with. If you have gear you like, it stays in the design. If we recommend a different model, we&rsquo;ll tell you why &mdash; and price the difference."),
    ("What about cloud subscriptions?", "We build local-first for the parts that matter: local recording, local AI, local control. The only cloud touch we use is a secure tunnel for remote access &mdash; and we tell you, in plain English, exactly what goes where."),
    ("Can you work with my existing smart home?", "Yes. That&rsquo;s what the Add-On and Existing-Upgrade plans are for. We audit, adopt, fix, and unify &mdash; we don&rsquo;t rip and replace what&rsquo;s working."),
    ("How long does the support relationship last?", "Indefinitely. The residency plan is month-to-month, and you hold the admin key from day one. If you ever leave, the system keeps working &mdash; you own it."),
    ("What do we do about firmware updates that break things?", "We watch the firmware stream for the devices in your install. When a major update lands, we test it on a staging rig before we push it to your home &mdash; and we roll back the moment we see a regression."),
]
body2 = '<section class="page-hero"><div class="wrap"><span class="kicker">Support</span><h1>Frequently asked questions</h1><p>The things every new homeowner asks before we start. If yours isn&rsquo;t here, call us.</p></div></section>'
body2 += '<section class="block"><div class="wrap">'
for q, a in faq:
    body2 += f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>'
body2 += '</div></section>'
body2 += '<section class="block"><div class="wrap"><div class="cta-band"><h2>Still have a question?</h2><p>Call or email &mdash; we answer.</p><div class="hero-ctas"><a class="btn btn-primary" href="../contact/">Contact us</a></div></div></div></section>'
write("support/faq/index.html",
      head("FAQ — SmartiHats", "Answers to the questions every homeowner asks: install process, ownership, firmware, cloud, support tiers, and what your data looks like.",
           base="../../") + b + body2 + footer(base="../../"))

# ================= SERVICE AREA =================
b = crumbs("../", "support", "Service Area")
body = '<section class="page-hero"><div class="wrap"><span class="kicker">Support</span><h1>Service area</h1><p>Sandy Springs &amp; Metro Atlanta. Here&rsquo;s the coverage map and what&rsquo;s on-site and what&rsquo;s remote.</p></div></section>'
body += '<section class="block"><div class="wrap"><div class="grid grid-2"><article class="card"><h3>📍 On-site coverage</h3><p>Sandy Springs, Buckhead, Dunwoody, Roswell, Alpharetta, Peachtree Corners, Marietta, and surrounding Metro Atlanta. We live here &mdash; same-day on-site service is the default on the residency plan.</p></article><article class="card"><h3>🌐 Remote coverage</h3><p>Anything inside the U.S. where a SmartiHats system is already installed. Remote diagnostics, monitoring, and on-call support are available anywhere with an internet connection.</p></article></div></div></section>'
body += '<section class="block tight"><div class="wrap"><div class="prose"><h2>Why coverage matters more than you think</h2><p>A smart-home team that&rsquo;s a flight away can fix your firmware, but they can&rsquo;t reach your wiring. When the lock is stuck or the camera is dead, the only fix that works is someone on site &mdash; and that someone has to live near you. That&rsquo;s the whole point of being local.</p></div></div></section>'
body += band("../../")
write("support/service-area/index.html",
      head("Service Area — Sandy Springs & Metro Atlanta",
           "On-site for the Metro Atlanta area, remote coverage anywhere in the U.S. Same-day service is the default on the residency plan.",
           base="../../") + b + body + footer(base="../../"))

# ================= CONTACT =================
b = crumbs("../", "support", "Contact")
body = '<section class="page-hero"><div class="wrap"><span class="kicker">Support</span><h1>Contact us</h1><p>One number that answers, one email, one line for existing customers. No menu, no queue.</p></div></section>'
body += '<section class="block"><div class="wrap"><h2>Four ways in, one answer</h2><div class="grid grid-2">'
body += '<article class="card"><h3>📞 Phone</h3><p>Mon–Fri, 8am–6pm ET. The number is on your onboarding email &mdash; a person, not a menu, is on the other end.</p></article>'
body += '<article class="card"><h3>✉️ Email</h3><p>For proposals, quotes, and non-urgent questions. We reply within one business day.</p></article>'
body += '<article class="card"><h3>🚨 Existing customer</h3><p>For anything that&rsquo;s broken <em>right now</em>: the on-call number from your onboarding email is the fastest route. We know your home, so the fix is faster &mdash; no re-discovery.</p></article>'
body += '<article class="card"><h3>🏠 Existing customer</h3><p>New install, new home, new build &mdash; book a free consultation and we&rsquo;ll walk the space before you commit.</p><p><a class="btn btn-primary" href="../../book/">Book a consultation</a></p></article>'
body += '</div></div></section>'
write("support/contact/index.html",
      head("Contact — SmartiHats",
           "One number that answers, one email, one line for existing customers. No menu, no queue.",
           base="../../") + b + body + footer(base="../../"))

print("pricing/support OK")
