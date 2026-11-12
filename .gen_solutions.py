"""Build solutions hub + 6 detail pages."""
import sys, os
sys.path.insert(0, "/home/dad/smartihats-site")
from gen_helpers import head, footer

ROOT = "/home/dad/smartihats-site"
def write(rel, content):
    p = os.path.join(ROOT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(content); print("wrote", rel, len(content))

def band(base):
    return ('<section class="block"><div class="wrap"><div class="cta-band">'
            '<h2>Turn your home into the easy one</h2>'
            '<p>A free on-site consultation maps your space, your gear, and your goals into a fixed-scope plan.</p>'
            f'<div class="hero-ctas"><a class="btn btn-primary" href="{base}book/">Book a free consultation</a>'
            f'<a class="btn btn-ghost" href="{base}demo/">Watch the demo</a></div></div></div></section>')

def crumbs(base, sec, page):
    return (f'<nav class="crumbs" aria-label="Breadcrumb"><a href="{base}">Home</a> &rsaquo; '
            f'<a href="{base}{sec}/">{sec.capitalize()}</a> &rsaquo; {page}</nav>')

# ================= HUB =================
items = [
    ("existing-upgrade", "Upgrade Your Existing Smart Home", "Already have cameras, locks, or a thermostat? We adopt what works, fix the gaps, and unify the rest into one app."),
    ("whole-home", "Whole-Home New Build", "Design the whole thing before the walls go up. Wiring, power, placement, and scenes &mdash; engineered first, purchased second."),
    ("single-feature", "Single-Feature Add-Ons", "Just want a face-recognition doorbell, or one smart lighting zone? A focused add-on that fits in a day or two."),
    ("local-responder", "The Local-After-Responder", "A partner who actually lives in Metro Atlanta when something breaks &mdash; not a vendor in another time zone."),
    ("data-ownership", "Data Ownership & Privacy", "Local storage, local AI, and an honest conversation about exactly where your footage and routines live."),
    ("rental-turn", "Rental / Turnover Package", "Hand tenants a home that runs itself &mdash; and keep full oversight from wherever you are."),
]
body = '<section class="page-hero"><div class="wrap"><span class="kicker">Solutions</span><h1>How we actually help</h1><p>Every engagement starts the same way: we listen, walk the space, and design around your life. Here are the ways that usually shows up.</p></div></section>'
body += '<section class="block"><div class="wrap"><h2>Six ways we&rsquo;re usually engaged</h2><div class="grid grid-3">'
for slug, t, d in items:
    body += f'<article class="card"><h3>{t}</h3><p>{d}</p><p><a class="card-link" href="{slug}/">{t} &rarr;</a></p></article>'
body += '</div></div></section>' + band("../")
write("solutions/index.html",
      head("Solutions — upgrades, new builds, add-ons, local support",
           "Smart home solutions in Metro Atlanta: existing upgrades, whole-home new builds, single-feature add-ons, local support, data ownership, and rentals.",
           base="../", active="solutions") + body + footer(base="../"))

# ================= DETAIL PAGES =================
def detail(page, title, tag, cards, prose, callout):
    c = crumbs("../../", "solutions", title)
    c += '<section class="page-hero"><div class="wrap"><span class="kicker">Solution</span><h1>' + title + "</h1>"
    c += '<p>' + tag + '</p></div></section>'
    c += '<section class="block"><div class="wrap"><h2>What this engagement looks like</h2><div class="grid grid-2">'
    for h, p in cards:
        c += f'<article class="card"><h3>{h}</h3><p>{p}</p></article>'
    c += '</div></div></section>'
    c += '<section class="block tight"><div class="wrap"><div class="prose">'
    for h3, p in prose:
        c += f'<h2>{h3}</h2><p>{p}</p>'
    c += f'<div class="callout">{callout}</div></div></div></section>'
    c += band("../../")
    return c

write("solutions/existing-upgrade/index.html",
      head("Upgrade Your Existing Smart Home",
           "Bring your existing cameras, locks, and thermostats into one working, supported system — keep what’s good, fix the rest.",
           base="../../") + detail(
        "existing-upgrade", "Upgrade Your Existing Smart Home",
        "You don’t need to throw things away. We audit what you own, rescue the pieces that are worth keeping, and build a clean, unified system around them.",
        [("💳 No rip-and-replace", "We start with what you already have. A working camera or lock stays in play when it makes sense — no wasteful full teardown."),
         ("🧱 Gap analysis", "We map what’s missing: a smart hub, proper local storage, scenes that actually span rooms, backup power where it matters."),
         ("🔗 Unified control", "Whatever survives the audit is commissioned into the same single app, so you stop toggling between old brands and new ones."),
         ("📄 Written handoff", "You get a document: what we found, what we changed, what we left alone, and why. No mystery, no black box.")],
        [("A two-part process", "First we audit and scope. Then we execute — usually in one or two focused weeks, with a hard stop on your calendar."),
         ("What “adopted” means", "Adoption means it’s documented, tested to spec, and folded into the single app. If a device can’t be safely adopted, we tell you that and why, with the replacement option priced in."),
         ("Your devices, still yours", "Nothing we install locks you in. The gear you bought stays yours; the gear we add comes with a clear ownership model.")],
        '<div class="callout-title">Good for…</div><p>Homes that have “smart” devices but no plan. If you have cameras in one corner and a thermostat app you barely remember, this is the fix.</p>') + footer(base="../../"))

write("solutions/whole-home/index.html",
      head("Whole-Home New Build",
           "Design a smart home before the walls go up — wiring, power, placement, and scenes engineered from day one.",
           base="../../") + detail(
        "whole-home", "Whole-Home New Build",
        "New construction is the best time to do this right. We design the wiring, the power, and the placement before anything is purchased — so the smart home is part of the architecture, not a retrofit.",
        [("📐 Pre-frame design", "Before drywall, we decide where cameras, sensors, and access points go. Every device has network and power — not a power strip on the floor."),
         ("🔌 Right-sized network", "Wi-Fi, Ethernet backbone, and local storage sized for the number of devices you’ll actually have in two years."),
         ("🎬 Scenes and routines first", "We design the day you want to live in before we design the gear that enables it. The room tells us the device — not the other way round."),
         ("🔑 Day-one handoff", "At walk-through, the whole home works from one app, and you’re shown every routine. Not a demo — a test drive.")],
        [("What we deliver at build-out", "A smart-home schedule that runs alongside the general contractor: low-voltage wiring, camera placement, network backbone, and local storage — all coordinated so nothing gets painted over or buried."),
         ("Why pre-frame is not optional", "Retrofits force compromises: extra conduit runs, underpowered circuits, cameras in the wrong spot. A pre-frame smart home gets the right wiring and the right placement, with no trade-offs."),
         ("Pricing model", "Because everything is scoped before install, you get a fixed-scope price. We know the square footage, the device count, and the labor — so you get one number, not a range with asterisks.")],
        '<div class="callout-title">Good for…</div><p>New builds and major remodels. If the builder hasn’t started low-voltage work yet, get us in the room now.</p>') + footer(base="../../"))

write("solutions/single-feature/index.html",
      head("Single-Feature Add-Ons",
           "Add one smart-home feature — face doorbell, a lighting zone, a lock — in a focused day or two.",
           base="../../") + detail(
        "single-feature", "Single-Feature Add-Ons",
        "Sometimes the ask is specific: “I want a face-recognition doorbell.” or “Just light the front walk better.” We do exactly that — a focused, documented install that fits in a day or two.",
        [("🎯 Focused scope", "One thing, done well and documented. No upselling, no scope creep, no “while we’re in there…” surprises on the invoice."),
         ("🔌 Clean install", "Proper power, proper network, proper documentation. Even a single device deserves a clean job — the difference between a toy and an asset."),
         ("🧩 Ready to join the bigger picture", "When you want to expand, the add-on is already commissioned into the platform. Adding the second room on a Friday is a 2-hour job, not a new project."),
         ("📄 Documented", "You get the same written handoff as a whole-home build: what we installed, where it lives, how to reach it.")],
        [("Examples of single-feature installs", "Face-recognition doorbell · a smart lighting zone in the front entry · a smart lock on the back door · a single camera on the garage · a smart thermostat swap · an occupancy sensor in one room."),
         ("Why this beats a DIY kit", "A DIY kit gets you to working. SmartiHats gets you to supported. The device is placed right, powered right, commissioned right, and someone local knows it by name."),
         ("Turnaround", "Most single-feature installs are scoped in a 20-minute call and installed within the week. We keep a small buffer for supply and weather, but the install day itself is one or two.")],
        '<div class="callout-title">Good for…</div><p>A specific improvement you’ve wanted for a while but don’t want a whole renovation to get.</p>') + footer(base="../../"))

write("solutions/local-responder/index.html",
      head("The Local After-Responder",
           "When your smart home breaks, a person who lives in Metro Atlanta can actually be there — not a ticket in a queue.",
           base="../../") + detail(
        "local-responder", "The Local After-Responder",
        "The most underrated part of a smart home is who answers when it breaks. We’re a team that lives in the homes we service — when a call comes in, the answer is a person, not a queue in another time zone.",
        [("📞 One number that answers", "You tell us what’s happening. A human who’s trained on your specific build is on the other end. No “press 4” menu-maze."),
         ("🚗 On-site within the day", "For the things that need a pair of hands in your home — a dead camera, a bad switch, a firmware update that broke a scene — we can usually be on site the same day."),
         ("🔁 Proactive fixes", "We watch the stack, see the firmware updates that tend to misbehave in local hardware, and apply safe fixes before they land on you at 2 a.m."),
         ("🤝 Ownership stays yours", "Support isn’t a lock. We hold your admin access for maintenance, but you always have the key. If you ever leave, you keep the system, and it keeps working.")],
        [("What the “after” actually includes", "Monitoring, diagnostics, the same-day on-site visit when needed, firmware and security patch watch, and one number that answers. The scope is yours to choose — from light monitoring to full coverage."),
         ("The 2 a.m. problem, solved", "Smart homes often break at the worst possible times: a lock that won’t unlock, a garage door that’s stuck, a thermostat that resets to 72. When you don’t have a local on-call, you’re troubleshooting in the dark. That’s the gap we fill."),
         ("Pricing model", "Residency is a flat, simple price that scales with the size of your install. We tell you exactly what’s included when we send you the proposal.")],
        '<div class="callout-title">Good for…</div><p>Anyone who values a supported smart home over a well-configured one. If the thought of a 3 a.m. garage-door failure keeps you up, this is the fix.</p>') + footer(base="../../"))

write("solutions/data-ownership/index.html",
      head("Data Ownership & Privacy",
           "Local storage, local AI, and an honest conversation about where your footage and routines actually live.",
           base="../../") + detail(
        "data-ownership", "Data Ownership & Privacy",
        "Your smart home is not supposed to be a data center. We design systems where your recordings, routines, and AI models stay in your home — and we tell you, in plain English, exactly where everything lives.",
        [("📼 Local storage", "Cameras record to storage in your home. Playback stays available when the internet — or a cloud provider — is down."),
         ("🧠 Local AI (when it makes sense)", "Face-recognition and anomaly detection are opt-in, per residence, and run on hardware you own. What it sees, it sees locally."),
         ("🔒 No cloud hostage situation", "Nothing we install holds your data in a cloud vault that a provider can price up. Your recordings are yours, on your device, in your house."),
         ("📄 A clear data map", "We hand you a one-page diagram: what runs where, what goes to a cloud, and why. No mystery, no “trust us.”")],
        [("What we never do", "We never ship your camera feeds to a data center for storage. We never require a cloud subscription for basic playback. We never sell or share your data. Ever."),
         ("What we do do, and why", "Some features — like remote access when you’re outside your LAN — require a secure tunnel. We use them, but we build them in a way you can audit: the keys are yours, the paths are known, and the traffic is encrypted."),
         ("Privacy as a spec, not a vibe", "We treat privacy the way we treat power: something you decide on day one, in the design. Not a checkbox on the privacy page of a camera you bought in 2023.")],
        '<div class="callout-title">Good for…</div><p>Anyone who wants a smart home without renting their privacy. If you have cameras and a cloud subscription, let’s talk about what local storage would change.</p>') + footer(base="../../"))

write("solutions/rental-turn/index.html",
      head("Rental / Turnover Package",
           "A handoff that works: the tenant gets a home that runs itself, and you keep full oversight from anywhere.",
           base="../../") + detail(
        "rental-turn", "Rental / Turnover Package",
        "A well-run short-term rental is a smart home with a lease on it. We build for the turnover workflow in mind — lights, locks, and scenes that run on a schedule, and that you can observe and adjust from wherever you are.",
        [("🔑 Guest-ready handoff", "The tenant gets a home that runs itself: lights, thermostat, scenes, and a lock that works on day one. No “here’s the code sheet” scramble at check-in."),
         ("📡 Your oversight, preserved", "You keep full visibility: locks, cameras, and the status of every room. When a guest leaves, your view of the home stays exactly where you want it."),
         ("🔁 Turnover automation", "Scenes that run on schedule: lights on at dusk, locks secured, thermostat set to an energy-conscious value while the unit is unoccupied."),
         ("🛠️ Maintenance visibility", "A dead camera or a leak sensor is a notification you can act on — from anywhere in the world — before it becomes a lost booking or a water bill.")],
        [("The turnover problem, solved", "Rental owners live in the gap between “guest experience” and “asset maintenance.” When a smart home is bolted on without a plan, the owner ends up juggling apps, keys, and tenants. When it’s designed for the workflow, the same devices that delight the guest also monitor the asset."),
         ("What’s in the package", "Locks, cameras, local storage, scenes, and a monitoring workflow. Everything is documented so the owner (or a property manager) can hand it off to the next tenant without a re-orient."),
         ("Pricing model", "Flat, by unit. You know what it costs to bring a unit up to standard, and what it costs to keep it there.")],
        '<div class="callout-title">Good for…</div><p>Owners of rentals, short-term stays, and staffed properties. If you manage more than one unit, this is the multiplier.</p>') + footer(base="../../"))

print("solutions OK")
