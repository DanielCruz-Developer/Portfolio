<h1 align="center">DanielC · Portfolio</h1>

<p align="center">
  A credentials portfolio for an AI developer, with an AI assistant that answers
  questions about it.
</p>

<p align="center">
  <a href="https://danielcruz-developer.github.io/Portfolio/"><b>View the live site →</b></a>
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white">
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-34D399">
  <img alt="Hosting" src="https://img.shields.io/badge/hosted-GitHub%20Pages-181717?logo=github">
  <img alt="Backend" src="https://img.shields.io/badge/chat-Supabase%20Edge-3ECF8E?logo=supabase&logoColor=white">
</p>

---

## About

A single-page portfolio presenting eleven verifiable credentials in
retrieval-augmented generation, agentic AI and cybersecurity — built as a
static site that is **generated from Python** rather than written by hand.

The page is deliberately dependency-free: no framework, no bundler, no npm
install. A Python script renders a content file into one self-contained HTML
page, which GitHub Pages serves directly.

## Features

**Content as data.** Every word, credential and course lives in `content.py` as
plain Python. Adding a certificate is five lines and a rebuild — the card,
category filter and verification link are all generated.

**Grounded AI assistant.** A chat widget answers questions about the developer's
background using only the portfolio's own content as its system prompt, so it
cannot invent credentials. When it lacks an answer it says so and points to
email. The API key stays server-side in a Supabase Edge Function, rate-limited
per visitor.

**Motion that degrades gracefully.** Scroll reveals, a parallax hero, animated
counters and a scrolling marquee, driven by `IntersectionObserver` and CSS
transitions. Content is visible by default, so it still reads correctly with
JavaScript disabled or `prefers-reduced-motion` set.

**Project showcase.** Each project card opens an interactive demo page, and
hovering a card plays a live miniature of that page inside it. Cards take their
colors from the project, and the grid scales from two projects to many.

**Filterable credential gallery.** The IBM certificate card opens its own page
with the nine course certificates behind it, filterable by discipline, each
linking to its Coursera verification page.

**Responsive across resolutions.** Fluid type and layout from 375 px phones up
to 4K displays, where the whole layout scales rather than stranding the content
in the middle of the screen.

**Safe to edit.** The build refuses to run on a malformed content file or an
unknown course category, and writes nothing when it fails — a bad edit cannot
publish a broken page.

## How it works

```
content.py ──┐                  index.html
             ├──► build.py ──►  ibm-courses.html     ──► GitHub Pages
templates/ ──┘                  assistant-config.js           │
                                                              ▼
                                        chat widget ──► Supabase Edge Function
                                                              │
                                                              ▼
                                                         OpenRouter
```

`content.py` holds the data. `templates/page.html` holds the design — all CSS
and browser JavaScript. `build.py` renders one into the other and writes the two
files that get published.

Browser-side code stays JavaScript because browsers only execute JavaScript, but
it is generated output: maintaining the site means editing Python.

## Tech

| Layer | Built with |
|---|---|
| Site generator | Python 3.8+, standard library only |
| Page | Semantic HTML, CSS custom properties, vanilla JavaScript |
| Type | Space Grotesk · IBM Plex Sans · JetBrains Mono |
| Chat backend | Supabase Edge Function (Deno) proxying OpenRouter |
| Hosting | GitHub Pages |

## Credentials featured

- **IBM RAG and Agentic AI** — Professional Certificate, ten courses covering
  retrieval pipelines, vector databases, LangChain, LangGraph, CrewAI, AutoGen,
  BeeAI and MCP
- **Certificate in Cybersecurity Proficiency** — Concordia University,
  Continuing Education

Every code on the page resolves at
[coursera.org/verify](https://coursera.org/verify).

## Running it locally

```bash
python build.py
python -m http.server 8000
```

Then open <http://localhost:8000>.

Editing, publishing and troubleshooting are covered in
**[MAINTAINING.md](MAINTAINING.md)**.

## Contact

**Daniel Cruz** — AI Developer, Montreal
[danielcruzcastro30@gmail.com](mailto:danielcruzcastro30@gmail.com) ·
[LinkedIn](https://linkedin.com/in/daniel-cruz-0bab18224)
