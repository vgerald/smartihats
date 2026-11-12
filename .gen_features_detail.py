"""Build the 4 detailed feature pages."""
import sys, os
sys.path.insert(0, "/home/dad/smartihats-site")
from gen_helpers import head, footer, SITE, DATE

ROOT = "/home/dad/smartihats-site"

def write(rel, content):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        f.write(content)
    print("wrote", rel, len(content))

def base_section():
    return ('<section class="block"><div class="wrap"><div class="cta-band">'
            '<h2>See it working in your home</h2>'
            '<p>Book a free on-site visit and we&rsquo;ll walk you through the exact setup your space deserves.</p>'
            '<div class="hero-ctas"><a class="btn btn-primary" href="../../book/">Book a free consultation</a>'
            '<a class="btn btn-ghost" href="../../demo/">Watch the demo</a></div></div></div></section>')

def crumbs(base, section, page):
    return (f'<nav class="crumbs" aria-label="Breadcrumb">'
            f'<a href="{base}">Home</a> &rsaquo; '
            f'<a href="{base}{section}/">{section.capitalize()}</a> &rsaquo; {page}</nav>')

# ================= ONE APP CONTROL =================
b1 = crumbs("../../", "features", "One-App Control") + """
<section class="page-hero"><div class="wrap"><span class="kicker">Feature</span>
<h1>One app. Every device. Zero juggling.</h1>
<p>Your whole home &mdash; lights, locks, climate, cameras, garage, audio, and scenes &mdash; controlled from a single app. One login, one place to look, one number to call.</p></div></section>
<section class="block"><div class="wrap"><div class="grid grid-2">
  <article class="card"><h3>🎚️ Unified control</h3><p>Flip the porch light, lock the door, and drop the temp to 70 from one screen &mdash; no app switching, no &ldquo;is this the right login?&rdquo;</p></article>
  <article class="card"><h3>🔁 Scenes that just work</h3><p>One tap &mdash; <em>Movie Night</em>, <em>Away</em>, <em>Good Night</em> &mdash; orchestrates lights, locks, and heat together. Scenes are the whole point.</p></article>
  <article class="card"><h3>📱 Voice & automation included</h3><p>Connect your favorite voice assistant. Automations like &ldquo;when the door locks at night, run Good Night&rdquo; are built, not bolted on.</p></article>
  <article class="card"><h3>🧩 Mixed brands, one brain</h3><p>Zigbee, Z-Wave, WiFi, Matter &mdash; we speak every language your gear does and translate it into one clean interface.</p></article>
</div></div></section>
<section class="block tight"><div class="wrap"><div class="prose">
<h2>What this fixes for you</h2>
<p>Modern homes quietly accumulate a drawer of apps. Each one is a credential, a cloud dependency, and a support queue. When the power drops and everything half-restarts, you need eight apps to piece your home back together.</p>
<p>SmartiHats consolidates all of it into one platform you own. Every device we install is commissioned into that single app, tested end-to-end, and documented. If we ever add a capability, it lands inside the same app &mdash; not a new one on your home screen.</p>
<div class="callout"><div class="callout-title">The day-one test</div><p>Before we hand you the keys, we prove it: you run a full home tour from the one app, start to finish, while we watch. No &ldquo;that should work.&rdquo;</p></div>
</div></div></section>
""" + base_section()
write("features/one-app-control/index.html",
      head("One-App Control", "Control every light, lock, thermostat, camera, and scene from a single app — no drawer full of brand logins.",
           base="../../", active=None) + b1 + footer(base="../../"))

# ================= LOCAL AI =================
b2 = crumbs("../../", "features", "Local AI Automation") + """
<section class="page-hero"><div class="wrap"><span class="kicker">Feature</span>
<h1>Automation that thinks, locally.</h1>
<p>Smart routines that run on hardware in your home &mdash; faster response, complete privacy, and no cloud update that quietly breaks your morning.</p></div></section>
<section class="block"><div class="wrap"><div class="grid grid-2">
  <article class="card"><h3>👋 Face-recognition doorbell</h3><p>Know who&rsquo;s at the door &mdash; a face you know, a stranger, or nobody &mdash; before you answer. No stranger photos stored in a third party&rsquo;s cloud.</p></article>
  <article class="card"><h3>💡 Adaptive lighting</h3><p>Lights warm as evening settles, brighten on your way home, and go dark when no one&rsquo;s in the room. It learns your household&rsquo;s real rhythm.</p></article>
  <article class="card"><h3>🛡️ Anomaly watch</h3><p>&ldquo;Someone is standing in the yard at 3 a.m.&rdquo; is a notification you want. A dog in the bushes at 3 p.m. is one you don&rsquo;t. On-device models keep that call local.</p></article>
  <article class="card"><h3>🔒 Private by design</h3><p>Because the model runs in your home, your footage and routines never have to travel to &mdash; or be readable by &mdash; a data center.</p></article>
</div></div></section>
<section class="block tight"><div class="wrap"><div class="prose">
<h2>Why &ldquo;local&rdquo; is the whole point</h2>
<p>Cloud-only smart homes are brilliant until the outage hits, the provider changes its pricing, or a firmware push reshuffles your automations overnight. Local AI inverts the risk: the intelligence lives on your gear, in your home.</p>
<p>We provision the local compute, train the routines around <em>your</em> house and <em>your</em> people, then hand over the admin access. You keep the benefits of smart automation without renting them.</p>
<div class="callout ok"><div class="callout-title">Your data, your rules</div><p>Face recognition is opt-in, per residence. What it knows, it knows only where your hardware is.</p></div>
</div></div></section>
""" + base_section()
write("features/local-ai/index.html",
      head("Local AI Automation", "Face-recognition doorbell, adaptive lighting, and anomaly detection that runs on your own hardware — private, fast, and yours to own.",
           base="../../", active=None) + b2 + footer(base="../../"))

# ================= LOCAL RECORDING =================
b3 = crumbs("../../", "features", "Local-Recording Cameras") + """
<section class="page-hero"><div class="wrap"><span class="kicker">Feature</span>
<h1>Cameras you own. Recordings you keep.</h1>
<p>24/7 recording to storage in your home, with AI event detection &mdash; and without a monthly cloud vault you didn&rsquo;t sign up for.</p></div></section>
<section class="block"><div class="wrap"><div class="grid grid-2">
  <article class="card"><h3>📼 24/7 local recording</h3><p>Every camera writes to storage you control. Playback stays available even when the internet &mdash; or the provider &mdash; is down.</p></article>
  <article class="card"><h3>🔔 Smarter alerts</h3><p>Get notified for the events that matter &mdash; a person at the door, a car in the drive &mdash; not a push for every leaf that blows across the frame.</p></article>
  <article class="card"><h3>🔌 Power-loss resilience</h3><p>On a network outage, local cameras keep recording and stay viewable on your LAN. Your security system should not depend on the cloud staying up.</p></article>
  <article class="card"><h3>🛠️ No export maze</h3><p>Need the footage? It&rsquo;s on your device, in your home. No &ldquo;export your video&rdquo; workflow that costs extra or takes days.</p></article>
</div></div></section>
<section class="block tight"><div class="wrap"><div class="prose">
<h2>The hidden cost of cloud cameras</h2>
<p>Most &ldquo;smart&rdquo; cameras trade convenience for captivity: the best playback window is behind a subscription, the full history is in someone else&rsquo;s cloud, and the price is allowed to change any time. When privacy or pricing becomes a concern, you have very little to hold.</p>
<p>SmartiHats sizes local storage for the days and cameras you actually want, and connects detection to it. The result is a camera system that remains <em>yours</em> &mdash; in every sense &mdash; for the life of the home.</p>
<div class="callout"><div class="callout-title">Sized to fit</div><p>We size storage and retention to your budget and your comfort level &mdash; from a short rolling window to a multi-week archive.</p></div>
</div></div></section>
""" + base_section()
write("features/local-recording/index.html",
      head("Local-Recording Cameras", "Cameras that record to storage in your own home — 24/7, AI event detection, no cloud subscription, no export maze.",
           base="../../", active=None) + b3 + footer(base="../../"))

# ================= LIFETIME SUPPORT =================
b4 = crumbs("../../", "features", "Lifetime Local Support") + """
<section class="page-hero"><div class="wrap"><span class="kicker">Feature</span>
<h1>Support with a name and a local zip code.</h1>
<p>When your smart home misbehaves at 2&nbsp;a.m., you want a person who can actually reach it &mdash; not a ticket in a queue in another time zone.</p></div></section>
<section class="block"><div class="wrap"><div class="grid grid-2">
  <article class="card"><h3>📞 One number that answers</h3><p>A real human, trained on your specific setup, on the other end. No &ldquo;press 4 for smart home,&rdquo; no menu maze.</p></article>
  <article class="card"><h3>🚚 Metro Atlanta coverage</h3><p>We live here. When a visit is needed, one of ours can be at your door &mdash; not a contractor from three states away.</p></article>
  <article class="card"><h3>🔄 Firmware &amp; health watch</h3><p>We monitor the stack, watch for the updates that tend to misbehave, and apply safe fixes before they bite you.</p></article>
  <article class="card"><h3>🧑‍🤝‍🧑 Ownership on day one</h3><p>You hold the admin key. Support is a partnership, not a dependency &mdash; you can leave anytime, and you&rsquo;ll still own everything.</p></article>
</div></div></section>
<section class="block tight"><div class="wrap"><div class="prose">
<h2>&ldquo;Who do I call?&rdquo; is a question we eliminate</h2>
<p>Most smart-home installs are a great week followed by a support cliff: the installer&rsquo;s warranty lingers, the cloud provider&rsquo;s support is generic, and the actual wiring is a mystery. That&rsquo;s when &ldquo;smart&rdquo; homes become projects every homeowner is too busy to babysit.</p>
<p>SmartiHats is the opposite of that cliff. We remain the accountable owner of the system &mdash; we know your layout, your routines, and your hardware &mdash; and we stay reachable for as long as you own the home.</p>
<div class="callout ok"><div class="callout-title">No hostage situation</div><p>Support is a relationship, not a lock. Your credentials, your automation, your data &mdash; all of it stays yours.</p></div>
</div></div></section>
""" + base_section()
write("features/lifetime-support/index.html",
      head("Lifetime Local Support", "Support with a name and a local zip — one number that answers, Metro Atlanta coverage, and firmware health you can trust.",
           base="../../", active=None) + b4 + footer(base="../../"))

print("features detail OK")
