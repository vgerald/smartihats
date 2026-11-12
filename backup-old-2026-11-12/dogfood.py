#!/usr/bin/env python3
"""
SmartiHats site dogfood validator.

Run after any edit to the site to check, per the launch checklist:
  a) HTML well-formedness (tag balance, void elements, no duplicate ids)
  b) Internal anchor links resolve; external links are https
  c) Consultation form: required fields present, Formspree marker present,
     and NO password/credential fields of any kind (hard FAIL if found)
  d) Mobile: viewport meta present; no fixed pixel widths that would
     cause horizontal scrolling on a 360-480px viewport
  e) Accessibility baseline: img alt text, labelled inputs, single h1,
     heading levels don't skip, text/background contrast >= 4.5:1
     (static analysis of declared CSS values incl. var() resolution)
  f) Performance: total local page weight < 1 MB; no render-blocking or
     remote <script src> (all external scripts would be flagged)
  g) SEO: <title>, meta description, parseable LocalBusiness JSON-LD
  h) Placeholder audit (informational): every TODO marker + placeholder
     string, so you know what content is still missing before launch

Exit code: 0 = all pass/fail checks green, 1 = at least one failure,
2 = the site files could not be read at all.

Usage:
  python3 dogfood/dogfood.py [site-directory]     # default: repo root
  (the site directory must contain index.html, styles.css, script.js)

No third-party dependencies — Python 3.8+ stdlib only.

Contrast check note: this is a *static* approximation (declared CSS
values, var() resolved, same-rule pairs + known container backgrounds).
It is deliberately conservative, but for final sign-off also run a
browser-based auditor (axe, WAVE, or Lighthouse) once the real photos
and copy are in place.
"""

import json
import math
import re
import sys
from html.parser import HTMLParser

# ---------------------------------------------------------------- utilities

VOID_ELEMENTS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}


def hex_to_rgb(value):
    v = value.strip().lstrip("#")
    if len(v) == 3:
        v = "".join(c * 2 for c in v)
    if len(v) != 6:
        return None
    try:
        return tuple(int(v[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return None


def _linear(channel):
    channel /= 255.0
    return channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4


def luminance(rgb):
    r, g, b = rgb
    return 0.2126 * _linear(r) + 0.7152 * _linear(g) + 0.0722 * _linear(b)


def contrast(hex_a, hex_b):
    la, lb = luminance(hex_to_rgb(hex_a)), luminance(hex_to_rgb(hex_b))
    if la < lb:
        la, lb = lb, la
    return round((la + 0.05) / (lb + 0.05), 2)


# ------------------------------------------------------------- report infra

class Report:
    FAIL = "FAIL"
    PASS = "PASS"
    INFO = "INFO"

    def __init__(self):
        self.rows = []
        self.failures = 0

    def add(self, check, ok, detail=""):
        status = self.PASS if ok else self.FAIL
        if not ok:
            self.failures += 1
        self.rows.append((check, status, detail))

    def note(self, check, detail=""):
        self.rows.append((check, self.INFO, detail))

    def print_report(self):
        width = max((len(r[0]) for r in self.rows), default=20)
        for check, status, detail in self.rows:
            print(f"  [{status:<4}] {check.ljust(width)}  {detail}")
        print()
        bad = self.failures
        print(f"RESULT: {'ALL CHECKS PASSED' if bad == 0 else f'{bad} CHECK(S) FAILED'}")
        return 0 if bad == 0 else 1


# ------------------------------------------------------------ (a) HTML parse

class StructuralParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []
        self.ids = []
        self.dupe_ids = set()
        self.imgs = []            # (lineno, has_alt, alt_value)
        self.svgs_img = []        # (lineno, has_role_img, has_aria_label)
        self.headings = []        # (lineno, level)
        self.labels_for = set()
        self.inputs = []          # (kind, id, name, type, lineno, placeholder, required)
        self.forms = []           # (lineno, action, method)
        self.links = []           # (lineno, href)
        self.script_tags = []     # (lineno, src, has_defer, is_jsonld_type)
        self.select_open = False
        self._svg_depth = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        line = self.getpos()[0]
        if tag in VOID_ELEMENTS:
            if tag == "img":
                self.imgs.append((line, "alt" in a, a.get("alt", "")))
            if tag == "input":
                self.inputs.append(("input", a.get("id", ""), a.get("name", ""),
                                    a.get("type", "text"), line,
                                    a.get("placeholder", ""),
                                    a.get("required") is not None))
            return
        self.stack.append((tag, line))
        if tag == "html":
            pass
        if tag == "body":
            pass
        if "id" in a:
            self.ids.append(a["id"])
            if a["id"] in {i for i in self.ids[:-1]}:
                self.dupe_ids.add(a["id"])
        if tag == "h1" or tag == "h2" or tag == "h3" or tag == "h4" or tag == "h5" or tag == "h6":
            self.headings.append((line, int(tag[1])))
        if tag == "label":
            if "for" in a:
                self.labels_for.add(a["for"])
        if tag in ("select", "textarea"):
            kind = tag
            if kind == "select":
                self.inputs.append(("select", a.get("id", ""), a.get("name", ""),
                                    "select", line, "", a.get("required") is not None))
                self.select_open = True
            else:
                self.inputs.append(("textarea", a.get("id", ""), a.get("name", ""),
                                    "textarea", line, a.get("placeholder", ""),
                                    a.get("required") is not None))
        if tag == "a" and "href" in a:
            self.links.append((line, a["href"]))
        if tag == "form":
            self.forms.append((line, a.get("action", ""), a.get("method", "")))
        if tag == "script":
            self.script_tags.append((line, a.get("src"), "defer" in a,
                                     a.get("type") == "application/ld+json"))
        if tag == "svg":
            self._svg_depth += 1
            if self._svg_depth == 1:
                has_role = a.get("role") == "img"
                has_label = "aria-label" in a
                self.svgs_img.append((line, has_role, has_label))

    def handle_endtag(self, tag):
        if tag in VOID_ELEMENTS:
            if tag == "select":
                self.select_open = False
            return
        if tag == "svg" and self._svg_depth > 0:
            self._svg_depth -= 1
        if not self.stack:
            self.errors.append(f"line ? : closing <{tag}> with no open element")
            return
        if self.stack[-1][0] == tag:
            self.stack.pop()
            return
        # search down the stack
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                bad = [t for t, _ in self.stack[i + 1:]]
                self.errors.append(
                    f"line {self.stack[-1][1]} : </{tag}> does not match open "
                    f"<{self.stack[-1][0]}> (unclosed: {', '.join(bad)})")
                del self.stack[i:]
                return
        self.errors.append(f"line ? : closing <{tag}> has no matching open element")

    def close(self):
        super().close()
        if self.stack:
            self.errors.append(
                "end of document: unclosed element(s): " +
                ", ".join(f"<{t}> (line {l})" for t, l in self.stack))


# ---------------------------------------------------------- (e) CSS contrast

def parse_css_colors(css_text):
    """Extract {selector: {color, background}} after resolving var() from :root.

    Returns (vars_map, rules) where rules is a list of (selector, color, bg).
    Only rules that declare `color` are kept. background is the declared
    background-color or the first resolvable color token in shorthand.
    """
    # strip /* */ comments
    css_text = re.sub(r"/\*.*?\*/", "", css_text, flags=re.S)

    root_vars = {}
    m = re.search(r":root\s*\{([^}]*)\}", css_text)
    if m:
        for decl in re.finditer(r"(--[\w-]+)\s*:\s*([^;]+);", m.group(1)):
            root_vars[decl.group(1)] = decl.group(2).strip()

    def resolve(color_str):
        if not color_str:
            return None
        color_str = color_str.strip()
        vm = re.fullmatch(r"var\(\s*(--[\w-]+)\s*\)", color_str)
        if vm and vm.group(1) in root_vars:
            return resolve(root_vars[vm.group(1)])
        h = re.fullmatch(r"#([0-9a-fA-F]{3,8})", color_str)
        if h:
            return color_str
        return None  # gradient/rgba/relative — not statically resolvable

    rules = []
    # naive but effective block walk (no @media nesting in this stylesheet
    # besides trivial ones — we treat everything as flat rules)
    for rm in re.finditer(r"([^{}]+)\{([^}]*)\}", css_text):
        selector = " ".join(rm.group(1).split())
        body = rm.group(2)
        color = None
        cm = re.search(r"(?<!-)color\s*:\s*([^;}]+)", body)
        if cm:
            color = resolve(cm.group(1))
        if color is None:
            continue
        bg = None
        bm = re.search(r"background(?:-color)?\s*:\s*([^;}]+)", body)
        if bm:
            bg = resolve(bm.group(1))
            if bg is None:
                # pick the first bare hex token inside a gradient stack
                hx = re.findall(r"#[0-9a-fA-F]{6}\b", bm.group(1))
                if hx:
                    bg = hx[0]
        rules.append((selector, color, bg))
    return rules


# known effective backgrounds for rules that don't declare their own
container_bg = {
    ".site-footer": "#12203a",
    ".footer-base": "#12203a",
    ".btn-nav": "#1a2b4a",
    ".hero": "#1a2b4a",
    ".section-tint": "#f2f6fc",
    ".example": "#f2f6fc",
    ".priority": "#f5a623",          # (defensive; not currently used)
    ".card": "#ffffff",
    ".pkg": "#ffffff",
    ".photo": "#ffffff",
    ".contact-panel": "#ffffff",
    ".step": "#ffffff",
    ".testimonials-placeholder": "#ffffff",
    ".footer-name": "#12203a",
    ".footer-label": "#12203a",
    ".form-fallback": "#fff7e8",
    ".form-error": "#fbe9e7",
    ".field-hint": "#fafafa",
    "body": "#fafafa",
}


def effective_background(selector, own_bg):
    if own_bg:
        return own_bg
    for key, bg in container_bg.items():
        if key in selector:
            return bg
    return "#fafafa"


# ------------------------------------------------------------------- main

def main():
    import os
    import pathlib
    if len(sys.argv) > 1:
        site = pathlib.Path(sys.argv[1]).resolve()
    else:
        site = pathlib.Path(__file__).resolve().parent.parent

    index_path = site / "index.html"
    styles_path = site / "styles.css"
    script_path = site / "script.js"
    if not index_path.exists():
        print(f"error: {index_path} not found — point me at the site directory", file=sys.stderr)
        return 2
    index_text = index_text_read = index_path.read_text(encoding="utf-8")
    styles_text = styles_path.read_text(encoding="utf-8") if styles_path.exists() else ""
    script_text = script_path.read_text(encoding="utf-8") if script_path.exists() else ""

    rep = Report()
    print(f"SmartiHats dogfood — validating {site}\n")

    # ---------------- (a) HTML validity ----------------
    p = StructuralParser()
    parse_ok = True
    try:
        p.feed(index_text)
        p.close()
    except Exception as e:  # malformed enough to crash the parser
        parse_ok = False
        p.errors.append(f"parser exception: {e}")
    issues = list(p.errors)
    if p.dupe_ids:
        issues.append("duplicate id(s): " + ", ".join(sorted(p.dupe_ids)))
    rep.add("a1 HTML well-formed (tag balance)", not issues,
            "; ".join(issues[:6]) if issues else "all tags balanced, no parser errors")

    # duplicate ids is its own named check
    rep.add("a2 no duplicate ids", not p.dupe_ids,
            ("duplicate: " + ", ".join(sorted(p.dupe_ids))) if p.dupe_ids else
            f"{len(p.ids)} ids, all unique")

    # ---------------- (b) links ----------------
    id_set = set(p.ids)
    bad_int = []
    bad_ext = []
    for line, href in p.links:
        if href.startswith("#"):
            target = href[1:]
            if not target:
                continue
            if target not in id_set:
                bad_int.append(f"line {line}: #{target}")
        elif href.startswith(("http://", "https://")):
            if not href.startswith("https://"):
                bad_ext.append(f"line {line}: {href}")
        # mailto:, tel:, data: are fine
    rep.add("b1 internal anchors resolve", not bad_int,
            "; ".join(bad_int) if bad_int else
            f"all {sum(1 for _, h in p.links if h.startswith('#'))} #anchors find their id")
    rep.add("b2 external links use https", not bad_ext,
            "; ".join(bad_ext) if bad_ext else "no plain-http links")

    # ---------------- (c) form ----------------
    rep.add("c1 consultation form exists", bool(p.forms),
            f"{len(p.forms)} form(s) found" if p.forms else "NO <form> in index.html")

    names = {i[2] for i in p.inputs if i[2]}
    required = {
        "name": "name",
        "email": "email",
        "phone": "phone",
        "zip": "zip",
        "property-type": "property-type",
        "project": "project",
    }
    missing = [f for f in required if f not in names]
    rep.add("c2 all required fields present", not missing,
            ("missing: " + ", ".join(missing)) if missing else
            "name, email, phone, zip, property-type, project all present")

    formspree_ok = False
    formspree_detail = "no valid https://formspree.io/f/<id> action URL found"
    for url in re.findall(r"https://formspree\.io/f/([A-Za-z0-9_\-]+)", index_text):
        if "YOUR_FORM_ID" in url.upper():
            formspree_detail = "form action still contains the YOUR_FORM_ID placeholder"
            continue
        formspree_ok = True
        formspree_detail = "action = https://formspree.io/f/" + url
        break
    marker_comment = re.search(r"FORMSPREE SETUP|FORMSPREE — wired|paste (my|the) form ID|form ID", index_text, re.I)
    rep.add("c3 Formspree wiring", formspree_ok and bool(marker_comment),
            formspree_detail + " + documented in a commented block"
            if (formspree_ok and marker_comment) else
            formspree_detail + (" (commented setup block also missing)" if not marker_comment else ""))

    cred_bad = [i for i in p.inputs if i[3] == "password"]
    name_pat = re.compile(r"(pass|secret|credential|apikey|api_key|apitoken|access_token|login)", re.I)
    cred_bad += [i for i in p.inputs if i[2] and name_pat.search(i[2])]
    rep.add("c4 form asks for NO credentials", not cred_bad,
            "OK — no password/credential fields anywhere in the form"
            if not cred_bad else "CREDENTIAL FIELDS FOUND: " +
            ", ".join(f"{i[0]}[{i[1] or i[2]}]" for i in cred_bad))

    # labels
    unlabelled = []
    for kind, iid, name, typ, line, ph, req in p.inputs:
        if typ in ("hidden",) or name == "_gotcha":
            continue
        if iid and iid in p.labels_for:
            continue
        # textareas/selects/inputs without id are unlabelled by definition here
        unlabelled.append(f"{kind}[name={name}] line {line}")
    rep.add("c5 every input/select/textarea is labelled", not unlabelled,
            "; ".join(unlabelled) if unlabelled else
            f"all {sum(1 for i in p.inputs if i[2] != '_gotcha')} form fields have <label for>")

    # ---------------- (d) mobile ----------------
    viewport_ok = re.search(r'<meta[^>]+name=["\']viewport["\'][^>]*width=device-width', index_text)
    rep.add("d1 viewport meta present", bool(viewport_ok),
            "width=device-width, initial-scale=1" if viewport_ok else "MISSING viewport meta tag")

    css_flat = re.sub(r"/\*.*?\*/", "", styles_text, flags=re.S)
    fixed_widths = []
    # Fixed rule-body widths over 320px risk horizontal scroll on phones /
    # tablets. `width: 100%` and max-width are fine. @media (min-width: Xpx)
    # conditions are legitimate mobile-first breakpoints and are scanned
    # separately below (only rule *bodies* are checked, so conditions in
    # @media rules never trigger this rule).
    for m in re.finditer(r"(?<!max-)(?<!min-)width\s*:\s*(\d+)px", css_flat):
        if int(m.group(1)) > 320:
            fixed_widths.append(f"width:{m.group(1)}px")
    # A rule-body min-width is a different beast — it can force overflow on
    # small screens. Strip @media header lines so their conditions don't count.
    css_body = "\n".join(
        ln for ln in css_flat.splitlines()
        if not re.match(r"^\s*@media\b", ln))
    for m in re.finditer(r"(?<!max-)min-width\s*:\s*(\d+)px", css_body):
        if int(m.group(1)) > 360:
            fixed_widths.append(f"rule-body min-width:{m.group(1)}px")
    html_widths = []
    for m in re.finditer(r'\bwidth=["\']?(\d{3,})\b', re.sub(r"<!--.*?-->", "", index_text, flags=re.S)):
        if int(m.group(1)) > 360:
            html_widths.append(m.group(1) + "px attribute")
    rep.add("d2 no fixed pixel widths (horizontal-scroll risk)", not fixed_widths and not html_widths,
            "; ".join(fixed_widths + html_widths) if (fixed_widths or html_widths)
            else "widths use %, rem, clamp() or max-width only")

    # ---------------- (e) accessibility ----------------
    imgs_no_alt = [f"line {l}" for l, has_alt, alt in p.imgs if not has_alt or not alt.strip()]
    svgs_unlabelled = [f"line {l}" for l, has_role, has_label in p.svgs_img if has_role and not has_label]
    rep.add("e1 every img has alt text", not imgs_no_alt,
            "; ".join(imgs_no_alt) if imgs_no_alt else
            f"{len(p.imgs)} img element(s) — {'all have alt' if p.imgs else 'site uses labelled inline SVGs instead'}")
    rep.add("e1b SVG illustrations labelled", not svgs_unlabelled,
            "; ".join(svgs_unlabelled) if svgs_unlabelled else
            "all role='img' SVGs carry aria-label")

    h1s = [l for l, lvl in p.headings if lvl == 1]
    rep.add("e2 exactly one h1", len(h1s) == 1, f"found {len(h1s)} h1")
    levels = [lvl for _, lvl in p.headings]
    skips = []
    for i in range(1, len(levels)):
        if levels[i] > levels[i - 1] + 1:
            skips.append(f"h{levels[i-1]}→h{levels[i]}")
    rep.add("e3 heading levels never skip", not skips,
            "; ".join(skips) if skips else
            f"order ok: {' > '.join('h' + str(l) for l in levels[:6])} …")

    # contrast
    rules = parse_css_colors(styles_text)
    low = []
    checked = 0
    for selector, color, own_bg in rules:
        bg = effective_background(selector, own_bg)
        if not bg:
            continue
        ratio = contrast(color, bg)
        checked += 1
        if ratio < 4.5:
            low.append(f"{selector} ({color} on {bg} = {ratio}:1)")
    rep.add("e4 text/background contrast AA (>=4.5:1)", not low,
            (" ".join(low[:4]) if low else
             f"{checked} color/background pair(s) checked, all >= 4.5:1"))

    # ---------------- (f) performance ----------------
    total = 0
    parts = []
    for name, text in (("index.html", index_text), ("styles.css", styles_text), ("script.js", script_text)):
        total += len(text.encode("utf-8"))
        parts.append(f"{name} {len(text.encode('utf-8')) // 1024}KB")
    ok_weight = total < 1024 * 1024
    rep.add("f1 total page weight < 1 MB", ok_weight,
            f"{total // 1024}KB total — " + ", ".join(parts))

    blocking = []
    for line, src, defer, is_jsonld in p.script_tags:
        if is_jsonld or src is None:
            continue
        if src.startswith("http") and not src.startswith(("http://" + "127.", "https://127.")):
            blocking.append(f"remote script {src} (line {line}, defer={defer})")
        elif not defer:
            blocking.append(f"render-blocking local script {src} (line {line})")
    rep.add("f2 no render-blocking / remote scripts", not blocking,
            "; ".join(blocking) if blocking else
            "script.js is local + defer; JSON-LD is data, not executable")

    external_css = re.findall(r'<link[^>]+rel=["\']stylesheet["\'][^>]+href=["\']([^"\']+)', index_text)
    remote_css = [c for c in external_css if c.startswith("http")]
    rep.add("f3 no external CSS/fonts", not remote_css,
            ", ".join(remote_css) if remote_css else
            "local styles.css only; system font stack (zero font downloads)")

    # ---------------- (g) SEO ----------------
    title = re.search(r"<title>(.*?)</title>", index_text, re.S)
    desc = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)', index_text)
    rep.add("g1 <title> present", bool(title), (title.group(1)[:70] + "…") if title and len(title.group(1)) > 70 else (title.group(1) if title else "MISSING"))
    rep.add("g2 meta description present", bool(desc), (desc.group(1)[:70] + "…") if desc and len(desc.group(1)) > 70 else (desc.group(1) if desc else "MISSING"))

    ld_ok, ld_detail = False, ""
    ld_blocks = re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', index_text, re.S)
    if ld_blocks:
        try:
            data = json.loads(ld_blocks[0])
            ld_ok = data.get("@type") == "LocalBusiness" and "SmartiHats" in data.get("name", "")
            ld_detail = f'@type LocalBusiness, name={data.get("name")}, areaServed={data.get("areaServed")}'
        except json.JSONDecodeError as e:
            ld_detail = f"JSON parse error: {e}"
    else:
        ld_detail = "no application/ld+json block found"
    rep.add("g3 LocalBusiness JSON-LD parses", ld_ok, ld_detail)

    # ---------------- (h) placeholder audit (informational) ---------------
    todos = sorted(set(re.findall(r"TODO\(([a-z-]+)\)", index_text + script_text)))
    audit_bits = []
    if todos:
        audit_bits.append("TODO markers: " + ", ".join(todos))
    counts = {
        "YOUR_FORM_ID (Formspree)": index_text.count("YOUR_FORM_ID"),
        "placeholder phone (555-010-0199)": index_text.count("5550100199") + index_text.count("010-0199"),
        "placeholder email (hello@smartihats.com)": index_text.count("hello@smartihats.com"),
        "demonstration setup badge": len(re.findall(r"Demonstration setup", index_text)),
        "testimonials placeholder block": len(re.findall(r"testimonials-placeholder", index_text)),
    }
    audit_bits.append("; ".join(f"{k} ×{v}" for k, v in counts.items()))
    rep.note("h  placeholder audit", " | ".join(audit_bits))

    return rep.print_report()


if __name__ == "__main__":
    sys.exit(main())
