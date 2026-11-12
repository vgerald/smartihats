"""Build all 16 SmartiHats pages into ./out/ (mirrors site root)."""
import os, sys
from gen_helpers import head, footer, book_form, SITE, DATE

ROOT = "/home/dad/smartihats-site"
sys.path.insert(0, ROOT)

def write(rel, content):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        f.write(content)
    print("wrote", rel, len(content), "bytes")

# ---------------------------------------------------------------- LANDING
landing_body = """
<section class="hero">
  <div class="wrap">
    <span class="kicker">SmartiHats &middot; Smart &amp; Intelligent Home Automation &middot; Sandy Springs &amp; Metro Atlanta</span>
    <h1>One app for your whole home. <em>We build it, and we stay in your corner.</em></h1>
    <p class="hero-sub">SmartiHats designs, installs, and maintains a full smart-home stack &mdash; lights, locks, thermostat, cameras, scenes, and AI automation &mdash; from a single app, then stays as your local partner for life. Because the best time to fix a smart home is the 2&nbsp;a.m. the power comes back on, and we&rsquo;re already awake.</p>
    <div class="hero-ctas">
      <a class="btn btn-primary btn-big" href="book/">Book a free consultation</a>
      <a class="btn btn-ghost btn-big" href="demo/">Watch the demo</a>
    </div>
    <p class="hero-fine">Licensed &middot; insured &middot; resident on-site &middot; lifetime support</p>
  </div>
</section>

<section class="block" id="why">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker">The problem</span>
      <h2>Your smart home shouldn&rsquo;t live in six apps.</h2>
      <p>Every device ships with its own app, its own password, its own update schedule. They only break together &mdash; at the worst possible moment.</p>
    </div>
    <div class="switch-row">
      <span class="lbl">Before</span>
      <button class="switch" type="button" data-switch-target="trapFlip" aria-pressed="false" aria-label="Flip the comparison to SmartiHats" data-label-on="trapTitle" data-label-on-txt="After: SmartiHats" data-label-off-txt="Before: six apps">🔁</button>
      <span class="lbl" id="trapTitle">After: one app</span>
    </div>
    <div class="trap" id="trapFlip" aria-hidden="false">
      <div class="trap-col" aria-label="The sprawl before">
        <h3>The sprawl you&rsquo;re living with</h3>
        <p class="col-sub">Seven apps, seven logins, seven ways to fail.</p>
        <div class="app-row"><div class="app-ico">💡</div><div><div class="app-name">Lighting app</div><div class="app-note">&ldquo;Lights went out&rdquo;</div></div></div>
        <div class="app-row"><div class="app-ico">🌡️</div><div><div class="app-name">Thermostat app</div><div class="app-note">&ldquo;It reset to 72&rdquo;</div></div></div>
        <div class="app-row"><div class="app-ico">🔐</div><div><div class="app-name">Lock app</div><div class="app-note">&ldquo;Code doesn&rsquo;t work&rdquo;</div></div></div>
        <div class="app-row"><div class="app-ico">📷</div><div><div class="app-name">Camera app</div><div class="app-note">&ldquo;Cloud subscription due&rdquo;</div></div></div>
        <div class="app-row"><div class="app-ico">🚪</div><div><div class="app-name">Garage / door app</div><div class="app-note">&ldquo;Is it closed?&rdquo;</div></div></div>
        <div class="app-row"><div class="app-ico">🎵</div><div><div class="app-name">Audio app</div><div class="app-note">&ldquo;Pairing again&rdquo;</div></div></div>
        <ul class="pain-list">
          <li>Different cloud providers, different passwords</li>
          <li>No scene works across two brands at once</li>
          <li>Updates break automation at 3 a.m.</li>
          <li>Support = chat with a call center 9 hrs away</li>
        </ul>
      </div>
      <div class="arrow-col" aria-hidden="true">
        <svg viewBox="0 0 48 48" fill="none" aria-hidden="true"><path d="M10 24h26M26 16l8 8-8 8" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </div>
      <div class="trap-col one-app" aria-label="SmartiHats, one app">
        <div class="ring">
          <svg viewBox="0 0 40 40" role="img" aria-label="SmartiHats house mark"><path d="M20 5l14 9v21H6V14z" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="1.5"/><rect x="15" y="20" width="10" height="11" rx="1.5" fill="var(--accent)"/><circle cx="20" cy="11.5" r="2.2" fill="var(--accent-strong)"/></svg>
        </div>
        <h3 id="oneAppTitle">One app. Your whole home.</h3>
        <span class="badge">● online &middot; 47 devices &middot; all working</span>
        <div class="chip-row">
          <span class="chip">Lights</span>
          <span class="chip">Thermostat</span>
          <span class="chip">Locks</span>
          <span class="chip">Cameras</span>
          <span class="chip">Garage</span>
          <span class="chip">Audio</span>
          <span class="chip">Scenes</span>
          <span class="chip">Face&nbsp;recognition</span>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="block tight" id="pillars">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker">Why SmartiHats</span>
      <h2>Three things you&rsquo;ll feel on day one</h2>
    </div>
    <div class="grid grid-3">
      <article class="card">
        <span class="card-tag">Design</span>
        <h3>We build it right, not just installed</h3>
        <p>Every device is placed, wired for the right power, and paired into one unified app before you ever leave the room. No &ldquo;figure it out&rdquo; handoff.</p>
        <p><a class="card-link" href="features/">See what we build &rarr;</a></p>
      </article>
      <article class="card">
        <span class="card-tag">Local</span>
        <h3>Resident, not remote</h3>
        <p>We live in Metro Atlanta. When something breaks at 2&nbsp;a.m., there&rsquo;s a human on call who can be at your door &mdash; not a queue in another time zone.</p>
        <p><a class="card-link" href="solutions/local-responder/">Why local matters &rarr;</a></p>
      </article>
      <article class="card">
        <span class="card-tag">Owned</span>
        <h3>No subscription hostage situation</h3>
        <p>Cameras, recordings, and automations run on your own gear, in your home. We hand you the admin key on day one &mdash; you own it, forever.</p>
        <p><a class="card-link" href="features/local-recording/">Your data, your home &rarr;</a></p>
      </article>
    </div>
  </div>
</section>

<div class="wrap">
  <div class="cta-band">
    <h2>Ready when you are</h2>
    <p>Book a free on-site consultation. We walk the space, map your devices, and hand you a clear, fixed-scope proposal &mdash; no pressure, no retainer to start.</p>
    <div class="hero-ctas">
      <a class="btn btn-primary" href="#consultation">Book a consultation</a>
      <a class="btn btn-ghost" href="pricing/">See pricing first</a>
    </div>
  </div>
</div>
"""
landing_body += '<div class="wrap"><div class="form-wrap" id="consultation">' + book_form(form_id="landing") + '</div></div>'

landing = head("SmartiHats — One app for your whole home",
               "Smart home automation design, install, and support in Sandy Springs and Metro Atlanta. One app, local experts, and lifetime support.",
               base="", active=None) + landing_body + footer(base="")
write("index.html", landing)

# ---------------------------------------------------------------- FEATURES HUB
feat_items = [
    ("one-app-control", "One-App Control", "Every light, lock, thermostat, camera, and scene in a single app you actually enjoy using.",
     "Lights, locks, climate, cameras, audio, scenes, and automations &mdash; all controlled with one unified interface instead of a drawer full of brand apps."),
    ("local-ai", "Local AI Automation", "Smart routines that run on your own hardware &mdash; faster, private, and not held hostage by a cloud update.",
     "Face-recognition doorbell, adaptive lighting, occupancy-aware scenes, and anomaly detection &mdash; all on-device, all private."),
    ("local-recording", "Local-Recording Cameras", "Cameras that record to your own storage. No cloud subscription, no data export wall, no surprise price hike.",
     "24/7 recording to local storage, AI event detection, and instant push alerts when something unusual happens &mdash; without renting a cloud vault."),
    ("lifetime-support", "Lifetime Local Support", "We stay in your corner after the install. One call and a Metro Atlanta technician can be there &mdash; not a call center abroad.",
     "Resident engineers, on-call response, firmware watch, and a single number that answers. Support that scales with your home, not your subscription tier."),
]
fbody = '<section class="page-hero"><div class="wrap"><span class="kicker">Features</span><h1>What we build for you</h1><p>Each capability is designed, installed, tested, and documented &mdash; then handed to you with ownership. No black boxes, no vendor lock-in.</p></div></section>'
fbody += '<section class="block"><div class="wrap"><div class="grid grid-2">'
for slug, title, tag, desc in feat_items:
    fbody += f'<article class="card"><h3>{title}</h3><p>{desc}</p><p><a class="card-link" href="{slug}/">{title} &rarr;</a></p></article>'
fbody += '</div></div></section>'
fbody += '''<div class="wrap"><div class="cta-band"><h2>Not sure what you need yet?</h2><p>Tell us about your home and we&rsquo;ll map it. No obligation, no jargon, no &ldquo;let&rsquo;s get started.&rdquo;</p><div class="hero-ctas"><a class="btn btn-primary" href="../book/">Book a free consultation</a><a class="btn btn-ghost" href="../demo/">Watch the demo</a></div></div></div>'''
write("features/index.html",
      head("Features — One app, local AI, your data, lifetime support",
           "Explore SmartiHats features: one-app control, local AI automation, local-recording cameras, and lifetime local support.",
           base="../", active="features") + fbody + footer(base="../"))

print("OK so far")
