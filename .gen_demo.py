"""Build demo hub + 4 interactive demos."""
import sys, os
sys.path.insert(0, "/home/dad/smartihats-site")
from gen_helpers import head, footer

ROOT = "/home/dad/smartihats-site"
def write(rel, content):
    p = os.path.join(ROOT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(content); print("wrote", rel, len(content))

def band(base):
    return ('<section class="block"><div class="wrap"><div class="cta-band">'
            '<h2>Liked what you saw?</h2>'
            '<p>These demos are simplified versions of what we build on-site. Book a free consultation and we&rsquo;ll walk your home.</p>'
            f'<div class="hero-ctas"><a class="btn btn-primary" href="{base}book/">Book a free consultation</a>'
            f'<a class="btn btn-ghost" href="{base}pricing/">See pricing</a></div></div></div></section>')

def crumbs(base, page):
    return (f'<nav class="crumbs" aria-label="Breadcrumb"><a href="{base}">Home</a> &rsaquo; '
            f'<a href="{base}demo/">Demos</a> &rsaquo; {page}</nav>')

# ================= HUB =================
items = [
    ("scene-demos", "Scene Demos", "Movie Night, Away, Good Morning &mdash; try the scene toggles and watch the home respond."),
    ("smart-security-walk", "Smart Security Walkthrough", "Follow a simulated night: front door lock, porch cam, motion events, and the alert you&rsquo;d actually get."),
    ("voice-assistant-clone", "Voice Assistant Clone", "Type a command instead of saying it &mdash; see what the assistant does with your whole home in one breath."),
    ("daily-automation", "Daily Automation", "Watch a full day unfold: sunrise, commute, dinner, good night &mdash; the routines we build for real homes."),
]
body = '<section class="page-hero"><div class="wrap"><span class="kicker">Demos</span><h1>See it, then feel it</h1><p>These interactive demos are simplified versions of the real thing. Click around, flip the switches, type the commands &mdash; it&rsquo;s the same platform we build on-site.</p></div></section>'
body += '<section class="block"><div class="wrap"><h2>Four demos to try before you book</h2><div class="grid grid-2">'
for slug, t, d in items:
    body += f'<article class="card"><span class="card-tag">Interactive</span><h3>{t}</h3><p>{d}</p><p><a class="card-link" href="{slug}/">Open the demo &rarr;</a></p></article>'
body += '</div><div class="callout" style="margin-top:1.4rem"><div class="callout-title">FaceId demo &middot; live</div><p>Our flagship face-recognition product is live at <strong>faceid.smartihats.com</strong> &mdash; a working demo of the doorbell system we install. Open it in a new tab and try it against your own face camera. No account needed.</p></div></div></section>' + band("../")
write("demo/index.html",
      head("Interactive Demos — scenes, security, voice, daily automation",
           "Try SmartiHats scene demos, a smart-security walkthrough, a voice-assistant clone, and daily automation — before you book a consultation.",
           base="../", active="demo") + body + footer(base="../"))

# ================= SCENE DEMOS =================
scene_demo = '''
<div class="scene-stage" id="sceneStage" data-scene="off" aria-label="Home scene preview">
  <div class="room">
    <div class="furniture sofa" aria-hidden="true"></div>
    <div class="furniture lamp" aria-hidden="true"></div>
    <div class="furniture lamp side" aria-hidden="true"></div>
    <div class="furniture door" aria-hidden="true"><span class="door-knob"></span></div>
    <div class="furniture thermostat" aria-hidden="true"><b id="thermVal">70</b>°</div>
  </div>
  <div class="scene-status" aria-live="polite"><span id="sceneStatus">No scene active</span></div>
</div>
<div class="scene-controls">
  <button class="btn btn-scene" data-scene-btn="movie-night">🎬 Movie Night</button>
  <button class="btn btn-scene" data-scene-btn="away">🏠 Away</button>
  <button class="btn btn-scene" data-scene-btn="good-morning">🌅 Good Morning</button>
  <button class="btn btn-ghost" data-scene-btn="off">↺ Reset</button>
</div>
'''
write("demo/scene-demos/index.html",
      head("Scene Demos — interactive",
           "Try Movie Night, Away, and Good Morning scenes — watch the lights, thermostat, and doors respond in real time.",
           base="../../") +
      crumbs("../../", "Scene Demos") +
      '<section class="page-hero"><div class="wrap"><span class="kicker">Demo</span><h1>Scene Demos</h1><p>Click a scene and watch the house respond. This is a lightweight preview of the same scene engine we install at your home.</p></div></section>'
      '<section class="block"><div class="wrap"><div class="prose"><p>Scenes are the whole point of a unified smart home. Here are three we build for most homes:</p>'
      '<p><strong>Movie Night</strong> &mdash; lights dim to ~10%, side lamps go off, thermostat holds, doors lock.</p>'
      '<p><strong>Away</strong> &mdash; all non-security lights off, locks secured, cameras armed, thermostat to energy mode.</p>'
      '<p><strong>Good Morning</strong> &mdash; lights warm up gradually, thermostat to comfort, side lamps on, doors still locked until you unlock.</p></div></div></section>'
      '<section class="block tight"><div class="wrap">' + scene_demo + '</div></section>' +
      footer(base="../../"))

# ================= SMART SECURITY WALK =================
sec_demo = '''
<div class="timeline" id="secTimeline" aria-live="polite">
  <div class="tl-item"><span class="tl-time">11:02 PM</span><span class="tl-msg">Front door locked. All clear.</span><span class="tl-badge ok">Secured</span></div>
  <div class="tl-item"><span class="tl-time">11:18 PM</span><span class="tl-msg">Porch light off. Cameras armed.</span><span class="tl-badge ok">Armed</span></div>
  <div class="tl-item pending"><span class="tl-time">2:47 AM</span><span class="tl-msg">Motion detected at front walk…</span><span class="tl-badge warn">Alert</span></div>
  <div class="tl-item pending"><span class="tl-time">2:47 AM</span><span class="tl-msg">Face match: <em>stranger</em>. Local push alert sent.</span><span class="tl-badge bad">Alert</span></div>
  <div class="tl-item pending"><span class="tl-time">2:47 AM</span><span class="tl-msg">Recording saved to local storage (2:47–2:51 AM).</span><span class="tl-badge ok">Saved</span></div>
</div>
<button class="btn btn-primary" id="replaySec">↻ Replay the night</button>
'''
write("demo/smart-security-walk/index.html",
      head("Smart Security Walkthrough",
           "Follow a simulated night: door lock, porch cam, motion event, face recognition, and the local alert you'd get.",
           base="../../") +
      crumbs("../../", "Security Walkthrough") +
      '<section class="page-hero"><div class="wrap"><span class="kicker">Demo</span><h1>Smart Security Walkthrough</h1><p>Follow one night at a SmartiHats home, from &ldquo;lock up&rdquo; to &ldquo;no one&rsquo;s there.&rdquo; This is a timeline simulation of the same event flow we install.</p></div></section>'
      '<section class="block"><div class="wrap"><div class="prose"><p>Here&rsquo;s what a typical night actually looks like with our stack:</p>'
      '<p><strong>11:02 PM</strong> &mdash; You tap <em>Away</em> from the app. Doors lock, non-security lights off, cameras armed.</p>'
      '<p><strong>2:47 AM</strong> &mdash; Motion at the front walk. The local model identifies a <em>stranger</em>. You get a push alert with a short clip &mdash; no cloud round-trip, no &ldquo;please log in to view your video.&rdquo;</p>'
      '<p><strong>By 6:00 AM</strong> &mdash; You open the clip, see it&rsquo;s a neighborhood cat, archive it. The recording is on your local drive, ready when you need it.</p></div></div></section>'
      '<section class="block tight"><div class="wrap">' + sec_demo + '</div></section>' +
      footer(base="../../"))

# ================= VOICE ASSISTANT CLONE =================
va_demo = '''
<div class="va-stage">
  <div class="va-input-row">
    <input type="text" id="vaInput" placeholder="Try: &ldquo;set it to movie night&rdquo; or &ldquo;lock every door&rdquo;"
           aria-label="Type a voice command" autocomplete="off" />
    <button class="btn btn-primary" id="vaSend">Say it</button>
  </div>
  <div class="va-chips" aria-label="Suggested commands">
    <button class="chip chip-btn" data-cmd="movie-night">🎬 Movie night</button>
    <button class="chip chip-btn" data-cmd="away">🏠 Away</button>
    <button class="chip chip-btn" data-cmd="good-morning">🌅 Good morning</button>
    <button class="chip chip-btn" data-cmd="lights-off">💡 Lights off</button>
    <button class="chip chip-btn" data-cmd="lock-all">🔐 Lock every door</button>
    <button class="chip chip-btn" data-cmd="temp-72">🌡️ Set to 72°</button>
  </div>
  <div class="va-feed" id="vaFeed" aria-live="polite" aria-busy="false">
    <p class="va-empty">Type a command or tap a suggestion &mdash; the assistant will respond here.</p>
  </div>
</div>
'''
write("demo/voice-assistant-clone/index.html",
      head("Voice Assistant Clone",
           "Type a command and watch SmartiHats execute it across the whole home — scenes, locks, thermostat, and lights in one breath.",
           base="../../") +
      crumbs("../../", "Voice Assistant Clone") +
      '<section class="page-hero"><div class="wrap"><span class="kicker">Demo</span><h1>Voice Assistant Clone</h1><p>Type a command (or tap a suggestion) and see what the assistant does with your home in one breath. On-site it&rsquo;s spoken out loud; the responses are the same.</p></div></section>'
      '<section class="block"><div class="wrap"><div class="prose"><p>We build the voice layer on top of the same command engine our app uses. A few things it handles well in a real home:</p>'
      '<p><strong>Scenes</strong> &mdash; &ldquo;movie night&rdquo; orchestrates lights, locks, and thermostat together.</p>'
      '<p><strong>Multi-device</strong> &mdash; &ldquo;turn off everything but the bathroom&rdquo; is one command, not five.</p>'
      '<p><strong>State queries</strong> &mdash; &ldquo;is the back door locked?&rdquo; gets an answer, not a shrug.</p>'
      '<p><strong>Air quality</strong> &mdash; &ldquo;set the thermostat to 70&rdquo; just works, and the response tells you it did.</p></div></div></section>'
      '<section class="block tight"><div class="wrap">' + va_demo + '</div></section>' +
      footer(base="../../"))

# ================= DAILY AUTOMATION =================
daily_demo = '''
<h2 style="margin-bottom:.2rem">A full day, hour by hour</h2>
<p class="prose" style="max-width:46rem">The exact scene an install at 8 p.m. would trigger &mdash; play the day and watch the automation fire.</p>
<div class="day-stages" id="dayStages" aria-live="polite">
  <div class="day-card active"><span class="day-time">6:30 AM</span><h4>Good Morning</h4><p>Lights warm up gradually. Thermostat to 68. Doors remain locked until you unlock.</p></div>
  <div class="day-card"><span class="day-time">8:15 AM</span><h4>Commute</h4><p>Front door locks. Cameras arm. Thermostat drops to 65 for the day.</p></div>
  <div class="day-card"><span class="day-time">12:00 PM</span><h4>Midday</h4><p>Occupancy sensors report empty. No motion. All clear.</p></div>
  <div class="day-card"><span class="day-time">5:45 PM</span><h4>Coming Home</h4><p>Front lights warm up. Thermostat climbs to 70. Porch light on.</p></div>
  <div class="day-card"><span class="day-time">8:00 PM</span><h4>Dinner</h4><p>Kitchen lights to 80%. Side lamps on. Music low on the kitchen speaker.</p></div>
  <div class="day-card"><span class="day-time">11:30 PM</span><h4>Good Night</h4><p>All non-security lights off. Doors lock. Cameras arm. Thermostat to 66.</p></div>
</div>
<div class="day-controls">
  <button class="btn btn-primary" id="playDay">▶ Play the day</button>
  <button class="btn btn-ghost" id="pauseDay">⏸ Pause</button>
  <button class="btn btn-ghost" id="resetDay">↺ Reset</button>
  <span class="muted" id="dayStatus">Paused</span>
</div>
'''
write("demo/daily-automation/index.html",
      head("Daily Automation",
           "Watch a full day unfold at a SmartiHats home — sunrise, commute, dinner, good night — the routines we build for real homes.",
           base="../../") +
      crumbs("../../", "Daily Automation") +
      '<section class="page-hero"><div class="wrap"><span class="kicker">Demo</span><h1>Daily Automation</h1><p>Here&rsquo;s what a typical day looks like with the routines we build. Press <em>Play the day</em> and watch the timeline advance.</p></div></section>'
      '<section class="block"><div class="wrap"><div class="prose"><p>The point of the demo is the <em>seamlessness</em>. None of these moments require you to open an app. The house handles itself on your schedule, and you only step in when you want to.</p>'
      '<p>Every one of these moments is a routine we can configure to your real life: your commute times, your kids&rsquo; bedtime, your thermostat preferences, your cameras&rsquo; armed windows.</p></div></div></section>'
      '<section class="block tight"><div class="wrap">' + daily_demo + '</div></section>' +
      footer(base="../../"))

print("demo OK")
