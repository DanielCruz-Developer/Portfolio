"""
Builds the portfolio site.

    python build.py

Reads your content from content.py, drops it into templates/page.html, and
writes out the two files GitHub Pages actually serves:

    index.html            the whole site
    ibm-courses.html      the courses page, opened from the IBM certificate
    assistant-config.js   the chatbot's knowledge and starter questions

You should not need to edit this file to change what the site says. Edit
content.py instead. This file only decides how that content becomes HTML.

Standard library only, so it runs on any Python 3.8+ with no pip install.
"""

import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

import content as C

ROOT = Path(__file__).parent
TEMPLATE = ROOT / "templates" / "page.html"
OUT_HTML = ROOT / "index.html"
OUT_COURSES = ROOT / C.COURSES_PAGE["file"]
OUT_CONFIG = ROOT / "assistant-config.js"

VERIFY_BASE = "https://coursera.org/verify/"


def esc(text):
    """Escape plain text so quotes, & and < are always safe to type."""
    return html.escape(str(text), quote=True)


# --------------------------------------------------------------------------
# Small reusable bits of markup
# --------------------------------------------------------------------------

CHECK_SVG = (
    '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" '
    'stroke="currentColor" stroke-width="2" stroke-linecap="round" '
    'stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>'
)
ARROW_DOWN_SVG = (
    '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" '
    'stroke="currentColor" stroke-width="2" stroke-linecap="round" '
    'stroke-linejoin="round"><path d="M12 5v14M19 12l-7 7-7-7"/></svg>'
)
MAIL_SVG = (
    '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" '
    'stroke="currentColor" stroke-width="2" stroke-linecap="round" '
    'stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/>'
    '<path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>'
)
LINKEDIN_SVG = (
    '<svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor">'
    '<path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.14 '
    '1.45-2.14 2.94v5.67H9.36V9h3.41v1.56h.05c.47-.9 1.63-1.85 3.36-1.85 3.6 0 '
    '4.27 2.37 4.27 5.45zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 '
    '4.12zM7.12 20.45H3.56V9h3.56zM22.22 0H1.77C.79 0 0 .77 0 1.72v20.55C0 '
    '23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.72C24 .77 23.2 0 '
    '22.22 0z"/></svg>'
)
SHIELD_SVG = (
    '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" '
    'stroke="currentColor" stroke-width="2" stroke-linecap="round" '
    'stroke-linejoin="round"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 '
    '1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 '
    '1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>'
    '<path d="m9 12 2 2 4-4"/></svg>'
)
ROBOT_SVG = (
    '<path d="M12 8V4"/><circle cx="12" cy="3" r="1"/>'
    '<rect width="16" height="12" x="4" y="8" rx="3"/><path d="M2 14h2"/>'
    '<path d="M20 14h2"/><path d="M9 12.5v2"/><path d="M15 12.5v2"/>'
)
SEND_SVG = (
    '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" '
    'stroke="currentColor" stroke-width="2" stroke-linecap="round" '
    'stroke-linejoin="round"><path d="m22 2-7 20-4-9-9-4z"/>'
    '<path d="M22 2 11 13"/></svg>'
)


def section_head(kicker, title_html=None, subtitle=None, style=""):
    attr = f' style="{style}"' if style else ""
    out = [f'    <div class="section-head"{attr} data-reveal>']
    out.append(f'      <div class="section-kicker">{esc(kicker)}</div>')
    if title_html:
        out.append(f'      <h2 class="section-title">{title_html}</h2>')
    if subtitle:
        out.append(f'      <p class="section-sub">{esc(subtitle)}</p>')
    out.append("    </div>")
    return "\n".join(out)


# --------------------------------------------------------------------------
# Section renderers
# --------------------------------------------------------------------------

def render_nav(home=""):
    """home is "" on the home page. Other pages pass "./" so the section links
    lead back to the home page instead of looking for sections on their own."""
    logo = C.NAV["logo"]

    def href(h):
        return home + h if home and h.startswith("#") else h

    links = "\n".join(
        f'      <a href="{esc(href(l["href"]))}">{esc(l["label"])}</a>'
        for l in C.NAV["links"]
    )
    cta = C.NAV["cta"]
    mobile_items = list(C.NAV["links"]) + [C.NAV["mobile_extra"]]
    mobile = "\n".join(
        f'  <a href="{esc(href(m["href"]))}">{esc(m["label"])}</a>' for m in mobile_items
    )
    aria = f'{logo["name"]} {logo["suffix"]}, ' + ("home page" if home else "back to top")
    return f"""<!-- ============ NAV ============ -->
<header class="nav" id="nav">
  <div class="container nav-inner">
    <a class="logo" href="{esc(home or "#top")}" aria-label="{esc(aria)}">
      <span class="dc">{esc(logo["name"])}</span><span class="dot">.</span><span class="pf">{esc(logo["suffix"])}</span>
    </a>
    <nav class="nav-links" aria-label="Primary">
{links}
      <a href="{esc(href(cta["href"]))}" class="nav-cta">{esc(cta["label"])}</a>
    </nav>
    <button class="burger" id="burger" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
</header>
<nav class="mobile-menu" id="mobileMenu" aria-label="Mobile">
{mobile}
</nav>"""


def render_hero():
    h = C.HERO
    tags = f'<span class="sep">/</span>\n      '.join(
        f"<span>{esc(t)}</span>" for t in h["tags"]
    )
    stats = "\n".join(
        '      <div class="stat"><div class="stat-num">'
        f'<span data-count="{int(s["value"])}">0</span>'
        + ('<span class="plus">+</span>' if s.get("plus") else "")
        + f'</div><div class="stat-label">{esc(s["label"])}</div></div>'
        for s in C.STATS
    )
    return f"""<!-- ============ HERO ============ -->
<section class="hero">
  <div class="hero-bg">
    <div class="hero-grid"></div>
    <div class="orb orb-1" data-orb="1"></div>
    <div class="orb orb-2" data-orb="2"></div>
  </div>
  <div class="container hero-content">
    <span class="hero-kicker" data-hero><span class="pulse-dot"></span>{esc(h["badge"])}</span>
    <h1>
      <span class="line"><span data-hero>{esc(h["name"])}</span></span>
      <span class="line"><span class="accent-line" data-hero>{esc(h["role"])}</span></span>
    </h1>
    <div class="hero-sub" data-hero>
      {tags}
    </div>
    <p class="hero-desc" data-hero>
      {h["description_html"]}
    </p>
    <div class="hero-actions" data-hero>
      <a class="btn btn-primary" href="{esc(h["primary_button"]["href"])}">
        {esc(h["primary_button"]["label"])}
        {ARROW_DOWN_SVG}
      </a>
      <a class="btn btn-ghost" href="{esc(h["ghost_button"]["href"])}">{esc(h["ghost_button"]["label"])}</a>
    </div>
    <div class="hero-stats" data-hero>
{stats}
    </div>
  </div>
  <div class="scroll-hint"><div class="mouse"></div><span>Scroll</span></div>
</section>"""


def render_marquee():
    items = "\n".join(
        f'    <span class="marquee-item">{esc(word)}</span>' for word in C.MARQUEE
    )
    return f"""<!-- ============ MARQUEE ============ -->
<div class="marquee" aria-hidden="true">
  <div class="marquee-track" id="marqueeTrack">
{items}
  </div>
</div>"""


def render_about():
    a = C.ABOUT
    paras = "\n".join(f"        <p>{p}</p>" for p in a["paragraphs_html"])
    points = "\n".join(
        f"""          <div class="about-point">
            {CHECK_SVG}
            <span>{esc(p)}</span>
          </div>"""
        for p in a["points"]
    )
    bullets = "\n".join(f"          <li>{esc(b)}</li>" for b in C.EXPERIENCE["bullets"])
    return f"""<!-- ============ ABOUT ============ -->
<section class="section" id="about">
  <div class="container">
{section_head(a["kicker"], a["title_html"])}
    <div class="about-grid">
      <div class="about-text" data-reveal>
{paras}
        <div class="about-points">
{points}
        </div>
      </div>
      <div class="exp-card" data-reveal>
        <div class="exp-role">{esc(C.EXPERIENCE["role"])}</div>
        <div class="exp-org">{esc(C.EXPERIENCE["org"])}</div>
        <ul class="exp-list">
{bullets}
        </ul>
      </div>
    </div>
  </div>
</section>"""


def _hex_rgb(value):
    """'#4C8DFF' -> '76,141,255', so CSS can build translucent glows from it."""
    h = value.lstrip("#")
    if not re.fullmatch(r"[0-9a-fA-F]{6}", h):
        sys.exit(f"build error: accent '{value}' must be a 6-digit hex color like #4C8DFF")
    return ",".join(str(int(h[i:i + 2], 16)) for i in (0, 2, 4))


def _slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _initials(title):
    """'Desktop Manager' -> 'DM', 'JobFinder' -> 'JF', 'Atlas' -> 'AT'."""
    words = title.split()
    if len(words) > 1:
        return (words[0][0] + words[1][0]).upper()
    caps = [ch for ch in title if ch.isupper()]
    return ("".join(caps[:2]) if len(caps) >= 2 else title[:2]).upper()


def _url(path):
    """Percent-encode a relative path (spaces in file names) but keep / and #."""
    return quote(path, safe="/#?=&")


ARROW_RIGHT_SVG = (
    '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" '
    'stroke="currentColor" stroke-width="2" stroke-linecap="round" '
    'stroke-linejoin="round"><path d="M5 12h14"/><path d="m13 6 6 6-6 6"/></svg>'
)


def render_projects():
    s = C.PROJECTS_SECTION
    projects = C.PROJECTS
    for p in projects:
        page = ROOT / p["page"].split("#")[0]
        if not page.exists():
            sys.exit(f"build error: project '{p['title']}' points at {p['page']}, which does not exist")
        if p.get("icon") and not (ROOT / p["icon"]).exists():
            sys.exit(f"build error: project '{p['title']}' icon {p['icon']} does not exist")

    categories = []
    for p in projects:
        if p["category"] not in categories:
            categories.append(p["category"])
    show_filters = len(projects) >= 3 and len(categories) >= 2
    # Cards sit two per row. A featured card takes a whole row, which only looks
    # right when the projects after it pair up; otherwise it renders like the rest.
    use_featured = (len(projects) - 1) % 2 == 0

    filters = ""
    if show_filters:
        buttons = ['      <button class="proj-filter active" data-filter="all">All '
                   f'<span>{len(projects)}</span></button>']
        for cat in categories:
            n = sum(1 for p in projects if p["category"] == cat)
            buttons.append(f'      <button class="proj-filter" data-filter="{_slug(cat)}">'
                           f'{esc(cat)} <span>{n}</span></button>')
        filters = ('    <div class="proj-filters" data-reveal role="group" aria-label="Filter projects">\n'
                   + "\n".join(buttons) + "\n    </div>\n")

    cards = []
    for p in projects:
        if p.get("icon"):
            mark = f'<img class="proj-icon" src="{esc(_url(p["icon"]))}" alt="" loading="lazy">'
        else:
            initials = _initials(p["title"])
            mark = f'<span class="proj-mono">{esc(initials)}</span>'
        facts = ""
        if p.get("metrics"):
            facts += ('<dl class="proj-metrics">' + "".join(
                f'<div><dt>{esc(v)}</dt><dd>{esc(label)}</dd></div>' for v, label in p["metrics"][:3]
            ) + "</dl>")
        if p.get("features"):
            facts += ('<ul class="proj-feats" aria-label="Features">'
                      + "".join(f"<li>{esc(f)}</li>" for f in p["features"]) + "</ul>")
        if facts:
            facts = f'<div class="proj-facts">{facts}</div>'
        stack = "".join(f"<li>{esc(t)}</li>" for t in p["stack"])
        status = (f'<span class="proj-status"><i></i>{esc(p["status"])}</span>'
                  if p.get("status") else "")
        preview = _url(p.get("preview") or p["page"])
        cls = "proj-card is-featured" if p.get("featured") and use_featured else "proj-card"
        cards.append(f"""      <article class="{cls}" data-cat="{_slug(p["category"])}" style="--pa:{esc(p["accent"])};--pa-rgb:{_hex_rgb(p["accent"])}" data-reveal>
       <div class="proj-tilt">
        <div class="proj-media" data-preview="{esc(preview)}">
          <div class="proj-cover" aria-hidden="true"><span class="proj-blob"></span><span class="proj-blob b2"></span>{mark}</div>
          {status}
          <span class="proj-live" aria-hidden="true"><i></i>Live preview</span>
        </div>
        <div class="proj-body">
          <div class="proj-meta"><span class="proj-cat">{esc(p["category"])}</span><span>{esc(p.get("year", ""))}</span></div>
          <h3 class="proj-title"><a class="proj-link" href="{esc(_url(p["page"]))}">{esc(p["title"])}</a></h3>
          <p class="proj-tagline">{esc(p["tagline"])}</p>
          <p class="proj-desc">{esc(p["description"])}</p>
          {facts}
          <ul class="proj-stack" aria-label="Built with">{stack}</ul>
          <span class="proj-cta" aria-hidden="true">Open the interactive demo {ARROW_RIGHT_SVG}</span>
        </div>
       </div>
      </article>""")

    count = f'<span class="proj-count">{len(projects):02d}</span>'
    head = section_head(s["kicker"], s["title_html"], s.get("subtitle"))
    head = head.replace(f'{esc(s["kicker"])}</div>', f'{esc(s["kicker"])} {count}</div>', 1)
    return f"""<!-- ============ PROJECTS ============ -->
<section class="section section-projects" id="projects">
  <div class="proj-backdrop" aria-hidden="true"></div>
  <div class="container">
{head}
{filters}    <div class="proj-grid" id="projGrid">
{chr(10).join(cards)}
    </div>
  </div>
</section>"""


def projects_for_assistant():
    """A plain-prose summary of the projects, appended to the chatbot's prompt so
    it can answer "what has he built?" without anyone retyping it."""
    parts = []
    for p in C.PROJECTS:
        feats = f" Features: {', '.join(p['features'])}." if p.get("features") else ""
        parts.append(
            f"{p['title']} ({p['category']}, {p.get('status', 'project')}): {p['tagline']} "
            f"{p['description']}{feats} Built with {', '.join(p['stack'])}."
        )
    return ("PROJECTS (each has an interactive demo page in the Projects section of "
            "the portfolio): " + " ".join(parts))


def render_credentials():
    s = C.CREDENTIALS_SECTION
    cards = []
    for c in C.CREDENTIALS:
        tags = "".join(
            f'<span class="tag{" blue" if t.get("style") == "blue" else ""}">'
            f'{esc(t["label"])}</span>'
            for t in c["tags"]
        )
        title = esc(c["title"])
        cta = ""
        if c.get("link"):
            title = f'<a class="cred-link" href="{esc(_url(c["link"]))}">{title}</a>'
            cta = (f'\n          <span class="cred-cta" aria-hidden="true">'
                   f'{esc(c.get("link_label", "Open"))} {ARROW_RIGHT_SVG}</span>')
        cls = "cred-card has-link" if c.get("link") else "cred-card"
        cards.append(f"""      <article class="{cls}" data-reveal>
        <div class="cred-img"><img src="{esc(c["image"])}" alt="{esc(c["alt"])}" loading="lazy"></div>
        <div class="cred-body">
          <div class="cred-tags">{tags}</div>
          <h3 class="cred-title">{title}</h3>
          <p class="cred-desc">
            {esc(c["description"])}
          </p>
          <div class="cred-meta">
            <span>{esc(c["issuer"])}</span>
            <span class="code">{esc(c["code"])}</span>
          </div>{cta}
        </div>
      </article>""")
    return f"""<!-- ============ FEATURED CREDENTIALS ============ -->
<section class="section section-alt" id="credentials">
  <div class="container">
{section_head(s["kicker"], s["title_html"], s.get("subtitle"))}
    <div class="featured-grid">
{chr(10).join(cards)}
    </div>
  </div>
</section>"""


def render_courses_hero():
    """The top of the courses page: the certificate the courses belong to."""
    pg = C.COURSES_PAGE
    cred = next((c for c in C.CREDENTIALS if c.get("link") == pg["file"]), None)
    if cred is None:
        sys.exit(f"build error: no credential has \"link\": \"{pg['file']}\", so "
                 "nothing on the home page opens the courses page")
    verify = f"{VERIFY_BASE}{cred['code']}"
    return f"""<!-- ============ CERTIFICATE ============ -->
<section class="cpage-hero">
  <div class="hero-bg"><div class="hero-grid"></div><div class="orb orb-1"></div></div>
  <div class="container cpage-grid">
    <div class="cpage-text" data-reveal>
      <a class="cpage-back" href="./#credentials">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5"/><path d="m12 19-7-7 7-7"/></svg>
        {esc(pg["back_label"])}</a>
      <div class="section-kicker">{esc(cred["issuer"])}</div>
      <h1 class="cpage-title">{esc(cred["title"])}</h1>
      <p class="cpage-desc">{esc(cred["description"])}</p>
      <a class="btn btn-ghost" href="{esc(verify)}" target="_blank" rel="noopener">
        {SHIELD_SVG}
        Verify {esc(cred["code"])}
      </a>
    </div>
    <div class="cpage-cert" data-reveal><img src="{esc(cred["image"])}" alt="{esc(cred["alt"])}"></div>
  </div>
</section>"""


def render_courses():
    s = C.COURSES_SECTION
    labels = {f["key"]: f["label"] for f in C.COURSE_FILTERS}

    filters = "\n".join(
        f'      <button class="filter-btn{" active" if i == 0 else ""}" '
        f'data-filter="{esc(f["key"])}">{esc(f["label"])}</button>'
        for i, f in enumerate(C.COURSE_FILTERS)
    )

    cards = []
    for c in C.COURSES:
        cat = c["category"]
        if cat not in labels:
            sys.exit(
                f"build error: course '{c['title']}' has category '{cat}', which is "
                f"not one of the COURSE_FILTERS keys {sorted(labels)}"
            )
        verify = f"{VERIFY_BASE}{c['code']}"
        cards.append(f"""      <article class="course-card" data-cat="{esc(cat)}" data-reveal>
        <div class="course-img"><img src="{esc(c["image"])}" alt="{esc(c["title"])} certificate" loading="lazy"></div>
        <div class="course-body">
          <span class="course-cat">{esc(labels[cat])}</span>
          <h3 class="course-title">{esc(c["title"])}</h3>
          <div class="course-meta"><span>{esc(c["date"])}</span><a href="{esc(verify)}" target="_blank" rel="noopener">{esc(c["code"])} &#8599;</a></div>
        </div>
      </article>""")

    return f"""<!-- ============ COURSES ============ -->
<section class="section" id="courses">
  <div class="container">
{section_head(s["kicker"], s["title_html"])}
    <div class="filters" data-reveal role="group" aria-label="Filter courses">
{filters}
    </div>
    <div class="courses-grid" id="coursesGrid">
{chr(10).join(cards)}
    </div>
  </div>
</section>"""


def render_skills():
    s = C.SKILLS_SECTION
    caps = "\n".join(
        f"""      <div class="cap-card" data-reveal>
        <span class="cap-num">/ {i:02d}</span>
        <h3 class="cap-title">{esc(cap["title"])}</h3>
        <p class="cap-desc">{esc(cap["description"])}</p>
      </div>"""
        for i, cap in enumerate(C.CAPABILITIES, start=1)
    )
    stack = "\n".join(
        f'      <div class="stack-card" data-reveal><div class="stack-name">'
        f'{esc(t["name"])}</div><div class="stack-role">{esc(t["role"])}</div></div>'
        for t in C.STACK
    )
    return f"""<!-- ============ CAPABILITIES ============ -->
<section class="section section-alt" id="skills">
  <div class="container">
{section_head(s["kicker"], s["title_html"], s.get("subtitle"))}
    <div class="cap-grid" id="capGrid">
{caps}
    </div>

{section_head(s["stack_kicker"], style="margin-top:96px")}
    <div class="stack-grid">
{stack}
    </div>
  </div>
</section>"""


def render_contact():
    c = C.CONTACT
    return f"""<!-- ============ CONTACT ============ -->
<section class="section" id="contact">
  <div class="container contact-wrap" data-reveal>
    <div class="section-kicker">{esc(c["kicker"])}</div>
    <h2 class="contact-title">{esc(c["title"])}<br><span class="hl">{esc(c["title_highlight"])}</span></h2>
    <p class="contact-sub">
      {esc(c["subtitle"])}
    </p>
    <div class="contact-actions">
      <a class="btn btn-primary" href="mailto:{esc(c["email"])}">
        {MAIL_SVG}
        {esc(c["email"])}
      </a>
      <a class="btn btn-ghost" href="{esc(c["linkedin"])}" target="_blank" rel="noopener">
        {LINKEDIN_SVG}
        {esc(c["linkedin_label"])}
      </a>
    </div>
    <div class="verify-note">
      {SHIELD_SVG}
      <span>{c["verify_note_html"]}</span>
    </div>
  </div>
</section>"""


def render_footer():
    links = "\n".join(
        f'      <a href="{esc(l["href"])}"'
        + ("" if l["href"].startswith("mailto:") else ' target="_blank" rel="noopener"')
        + f">{esc(l['label'])}</a>"
        for l in C.FOOTER["links"]
    )
    return f"""<footer>
  <div class="container footer-inner">
    <span class="copy">{esc(C.FOOTER["copy"])}</span>
    <div class="footer-links">
{links}
    </div>
  </div>
</footer>"""


def render_chat_widget():
    a = C.ASSISTANT
    return f"""<!-- ============ CHAT WIDGET ============ -->
<div class="chat-panel" id="chatPanel" role="dialog" aria-label="{esc(a["name"])}" aria-hidden="true">
  <div class="chat-header">
    <div class="chat-avatar">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{ROBOT_SVG}</svg>
    </div>
    <div>
      <div class="chat-name">{esc(a["name"])}</div>
      <div class="chat-status">{esc(a["status"])}</div>
    </div>
  </div>
  <div class="chat-body" id="chatBody">
    <div class="msg bot">{esc(a["greeting"])}</div>
    <div class="chat-suggestions" id="chatSuggestions">
      <span class="sug-label">Try asking</span>
    </div>
  </div>
  <div class="chat-input-row">
    <input class="chat-input" id="chatInput" type="text" placeholder="Type a question&#8230;" aria-label="Type a question">
    <button class="chat-send" id="chatSend" aria-label="Send message">
      {SEND_SVG}
    </button>
  </div>
</div>
<div class="chat-nudge" id="chatNudge" role="status">
  <span>{a["nudge_html"]}</span>
  <button class="nudge-close" id="nudgeClose" aria-label="Dismiss">&#10005;</button>
</div>
<button class="chat-fab" id="chatFab" aria-label="Open AI assistant" aria-expanded="false" title="Ask {esc(a["name"])}">
  <svg class="icon-chat" width="29" height="29" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ROBOT_SVG}</svg>
  <svg class="icon-close" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18M6 6l12 12"/></svg>
</button>"""


# --------------------------------------------------------------------------
# Build
# --------------------------------------------------------------------------

def build_assistant_config():
    """Write the chatbot's knowledge as a JS module the page imports.

    Values go through json.dumps, which produces valid JavaScript string and
    array literals, so any character you type in content.py is safe here.
    """
    a = C.ASSISTANT
    return (
        "// GENERATED BY build.py - DO NOT EDIT THIS FILE.\n"
        "// Change the assistant in content.py (the ASSISTANT section),\n"
        "// then run:  python build.py\n\n"
        f"export const suggestions = {json.dumps(a['suggestions'], indent=2)};\n\n"
        f"export const profile = {json.dumps(a['prompt'] + chr(10) * 2 + projects_for_assistant())};\n"
    )


def fill(page, replacements):
    for key, value in replacements.items():
        page = page.replace(f"<!--{{{key}}}-->", value)
    leftover = re.findall(r"<!--\{[A-Z_]+\}-->", page)
    if leftover:
        sys.exit(f"build error: template placeholders were not filled: {leftover}")
    return page


def main():
    if not TEMPLATE.exists():
        sys.exit(f"build error: missing template at {TEMPLATE}")

    template = TEMPLATE.read_text(encoding="utf-8")
    shared = {
        "OG_DESCRIPTION": esc(C.SITE["og_description"]),
        "FAVICON_INITIALS": esc(C.SITE["favicon_initials"]),
        "CHAT_URL": C.SITE["chat_url"],
        "FALLBACK_SUGGESTIONS": json.dumps(C.ASSISTANT["suggestions"]),
        "FOOTER": render_footer(),
        "CHAT_WIDGET": render_chat_widget(),
    }

    home = fill(template, dict(shared, **{
        "TITLE": esc(C.SITE["title"]),
        "DESCRIPTION": esc(C.SITE["description"]),
        "NAV": render_nav(),
        "MAIN": "\n".join([
            render_hero(), render_marquee(), render_about(), render_projects(),
            render_credentials(), render_skills(), render_contact(),
        ]),
    }))
    courses = fill(template, dict(shared, **{
        "TITLE": esc(C.COURSES_PAGE["title"]),
        "DESCRIPTION": esc(C.COURSES_PAGE["description"]),
        "NAV": render_nav(home="./"),
        "MAIN": "\n".join([render_courses_hero(), render_courses()]),
    }))

    OUT_HTML.write_text(home, encoding="utf-8", newline="\n")
    OUT_COURSES.write_text(courses, encoding="utf-8", newline="\n")
    OUT_CONFIG.write_text(build_assistant_config(), encoding="utf-8", newline="\n")

    print(f"wrote {OUT_HTML.name}  ({len(home):,} chars)")
    print(f"wrote {OUT_COURSES.name}  ({len(courses):,} chars)")
    print(f"wrote {OUT_CONFIG.name}")
    print(
        f"  {len(C.CREDENTIALS)} credentials, {len(C.COURSES)} courses, "
        f"{len(C.CAPABILITIES)} capabilities, {len(C.STACK)} stack entries"
    )


if __name__ == "__main__":
    main()
