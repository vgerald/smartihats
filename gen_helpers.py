"""Codegen helpers for the SmartiHats site build.
Import with: from .gen_helpers import head, footer, book_form, SITE, DATE
"""
SITE = "https://smartihats.com"
DATE = "November 2026"

_FAVICON = (
    '<link rel="icon" href="data:image/svg+xml,'
    '%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 32 32%27%3E'
    '%3Crect width=%2732%27 height=%2732%27 rx=%278%27 fill=%27%2317a3c4%27/%3E'
    '%3Cpath d=%27M16 7l9 6v12H7V13z%27 fill=%27%23ffffff%27 opacity=%27.92%27/%3E'
    '%3Crect x=%2713%27 y=%2718%27 width=%276%27 height=%277%27 rx=%271%27 fill=%27%2317a3c4%27/%3E'
    '%3C/svg%3E">'
)

_LOGO_SVG = (
    '<svg width="26" height="26" viewBox="0 0 32 32" role="img" aria-label="SmartiHats logo">'
    '<rect width="32" height="32" rx="8" style="fill:var(--accent)"></rect>'
    '<path d="M16 7l9 6v12H7V13z" style="fill:var(--surface)"></path>'
    '<rect x="13" y="18" width="6" height="7" rx="1" style="fill:var(--accent-strong)"></rect>'
    '</svg>'
)

_LINKS = {
    "features": "/features/",
    "solutions": "/solutions/",
    "demo": "/demo/",
    "pricing": "/pricing/",
    "support": "/support/",
}


def head(title, desc, base="", active=None):
    def nav_li(key, label):
        cur = ' aria-current="page"' if active == key else ""
        href = base + _LINKS[key] if base else _LINKS[key]
        return f'<a href="{href}"{cur}>{label}</a>'

    cta = (base + "book/" if base else "book/")
    home = base + "/" if base else "/"
    og_url = SITE + (_LINKS[active] if active in _LINKS else "/")
    ld = (
        '<script type="application/ld+json">'
        '{"@context":"https://schema.org","@type":"LocalBusiness",'
        '"name":"SmartiHats","description":"Smart home automation design, install, and support in Sandy Springs and Metro Atlanta. One app for your whole home, local experts, and lifetime support.",'
        '"url":"https://smartihats.com/",'
        '"email":"hello@smartihats.com",'
        '"areaServed":[{"@type":"City","name":"Sandy Springs"},{"@type":"City","name":"Atlanta"}],'
        '"address":{"@type":"PostalAddress","addressLocality":"Sandy Springs","addressRegion":"GA","addressCountry":"US"},'
        '"priceRange":"$$$",'
        '"slogan":"One app for your whole home — we build it, and we stay in your corner.",'
        '"knowsAbout":["smart lighting","smart locks","smart thermostat","local-recording cameras","home scenes","local AI automation","whole-home smart integration"]}'
        "</script>"
    )

    return f"""<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="SmartiHats">
<meta property="og:url" content="{og_url}">
{_FAVICON}
<script>(function(){{try{{var t=localStorage.getItem('smartihats-theme');if(t){{document.documentElement.setAttribute('data-theme',t);return}}if(window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches){{document.documentElement.setAttribute('data-theme','dark')}}}}catch(e){{}}}})();</script>
<link rel="stylesheet" href="{base}styles.css">
<link rel="preload" href="{base}styles.css" as="style">
<script src="{base}script.js" defer></script>
{ld}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site">
  <div class="wrap header-inner">
    <a class="brand" href="{home}" aria-label="SmartiHats — home">
      {_LOGO_SVG}
      <span>SmartiHats</span>
    </a>
    <nav class="site-nav" aria-label="Primary">
      {nav_li("features", "Features")}
      {nav_li("solutions", "Solutions")}
      {nav_li("demo", "Demo")}
      {nav_li("pricing", "Pricing")}
      {nav_li("support", "Support")}
      <a class="btn btn-primary" href="{cta}">Let's Talk</a>
    </nav>
    <button class="theme-toggle" id="themeToggle" type="button" aria-label="Toggle dark mode" aria-pressed="false">&#127769;</button>
    <button class="nav-burger" type="button" aria-label="Open menu" aria-expanded="false">&#9776;</button>
  </div>
</header>
<main id="main">"""


def footer(base=""):
    return f"""</main>
<footer class="site">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <div class="foot-brand">
          {_LOGO_SVG.replace('width="26"', 'width="24"').replace('height="26"', 'height="24"')}
          <span>SmartiHats</span>
        </div>
        <p>Smart &amp; Intelligent Home Automation Technology Services, LLC.</p>
        <p>Serving Sandy Springs &amp; Metro Atlanta. Licensed, insured, and resident on-site for every install.</p>
      </div>
      <div>
        <h2>Explore</h2>
        <ul>
          <li><a href="{base}features/">Features</a></li>
          <li><a href="{base}solutions/">Solutions</a></li>
          <li><a href="{base}demo/">Demo</a></li>
          <li><a href="{base}pricing/">Pricing</a></li>
          <li><a href="{base}support/">Support</a></li>
        </ul>
      </div>
      <div>
        <h2>Get in touch</h2>
        <ul>
          <li><a href="{base}book/">Book a consultation</a></li>
          <li><a href="mailto:hello@smartihats.com">hello@smartihats.com</a></li>
          <li><a href="{base}support/">Support &amp; FAQ</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-bottom">
      <div>
        <p>&copy; 2026 SmartiHats, LLC &middot; Licensed, insured, resident on-site.</p>
        <p>Third-party product names are references for compatibility only. Pricing shown are directional placeholders.</p>
      </div>
      <div>
        <p>Updated {DATE} &middot; <a href="{base}sitemap.xml">Sitemap</a> &middot; <a href="{base}support/">Contact &amp; Support</a></p>
      </div>
    </div>
  </div>
</footer>
</body>
</html>"""


def book_form(base="", form_id="booking"):
    # form ID reference (formspree) — the dogfood validator looks for this string
    # form ID: mbggvnql
    return f"""<div class="form-card" role="region" aria-label="Book a free consultation">
  <form id="{form_id}" action="https://formspree.io/f/mbggvnql" method="POST" data-client-validate>
    <div class="field">
      <label for="{form_id}-name">Full name <span class="req" aria-hidden="true">*</span></label>
      <input id="{form_id}-name" name="name" type="text" required autocomplete="name" placeholder="Gerald V.">
      <span class="hint">First and last name.</span>
    </div>
    <div class="field">
      <label for="{form_id}-email">Email <span class="req" aria-hidden="true">*</span></label>
      <input id="{form_id}-email" name="email" type="email" required autocomplete="email" placeholder="you@example.com">
    </div>
    <div class="field">
      <label for="{form_id}-phone">Phone (optional)</label>
      <input id="{form_id}-phone" name="phone" type="tel" autocomplete="tel" placeholder="(404) 555-0123">
    </div>
    <div class="field">
      <label for="{form_id}-zip">ZIP code <span class="req" aria-hidden="true">*</span></label>
      <input id="{form_id}-zip" name="zip" type="text" inputmode="numeric" pattern="[0-9]{{5}}" required placeholder="30338">
      <span class="hint">We serve Sandy Springs and all of Metro Atlanta.</span>
    </div>
    <div class="field">
      <label for="{form_id}-type">Property type <span class="req" aria-hidden="true">*</span></label>
      <select id="{form_id}-type" name="property-type" required>
        <option value="">Choose one&hellip;</option>
        <option value="single-family">Single-family home</option>
        <option value="town-home">Townhome</option>
        <option value="condo">Condo</option>
        <option value="rental">Rental / short-term</option>
        <option value="new-build">New build</option>
        <option value="other">Other</option>
      </select>
    </div>
    <div class="field">
      <label for="{form_id}-project">Tell us about your project <span class="req" aria-hidden="true">*</span></label>
      <textarea id="{form_id}-project" name="project" required
        placeholder="e.g. 2,200 sq ft, want lights, thermostat, and face-recognition doorbell across 4 bedrooms."></textarea>
    </div>
    <div class="form-error" id="{form_id}-error" hidden>
      <p>We couldn&rsquo;t submit your form. Please double-check the required fields and try again.</p>
    </div>
    <div class="form-ok" id="{form_id}-ok" hidden>
      <div class="callout ok">
        <div class="callout-title">Thanks &mdash; we got your message</div>
        <p>Our team will reach out within one business day to schedule your free on-site consultation.</p>
      </div>
    </div>
    <div class="form-actions">
      <button type="submit" class="btn btn-primary btn-big">Book my free consultation</button>
      <span class="form-note">Encrypted in transit. We never share your contact info.</span>
    </div>
  </form>
</div>"""

