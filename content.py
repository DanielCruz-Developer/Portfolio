"""
Everything that appears on the portfolio site lives in this file.

    Edit this file  ->  run  python build.py  ->  commit and push

That regenerates index.html and assistant-config.js for you. You never need to
open either of those files; they are build output.

A few conventions used below:

  * Fields whose name ends in _HTML may contain HTML tags, because the text
    needs them (for example <strong> to bold a few words, or <br> to force a
    line break). Everything else is plain text and is escaped automatically,
    so apostrophes, ampersands and quotes are always safe to type.
  * Dates and certificate codes are plain strings; nothing parses them.
  * To add something to a list, copy the last entry, paste it below, and edit
    the values. Trailing commas are fine and encouraged.
"""

# ---------------------------------------------------------------------------
# SITE  --  browser tab, search results, link previews
# ---------------------------------------------------------------------------

SITE = {
    "title": "DanielC | Portfolio",
    "description": (
        "Daniel Cruz, AI Developer in Montreal. RAG pipelines, agentic systems "
        "and cybersecurity. 11 verifiable credentials from IBM and Concordia "
        "University."
    ),
    "og_description": (
        "AI Developer · RAG & Agentic Systems · Cybersecurity · "
        "11 verifiable credentials."
    ),
    # Two letters drawn on the little browser-tab icon.
    "favicon_initials": "DC",
    # The chatbot backend (the Supabase function that holds the OpenRouter key).
    "chat_url": "https://kfhcaphutihlhuaalzjk.supabase.co/functions/v1/chat",
}

# ---------------------------------------------------------------------------
# NAV  --  the menu at the top. "href" points at a section id further down.
# ---------------------------------------------------------------------------

NAV = {
    "logo": {"name": "DanielC", "suffix": "Portfolio"},
    "links": [
        {"label": "About", "href": "#about"},
        {"label": "Projects", "href": "#projects"},
        {"label": "Credentials", "href": "#credentials"},
        {"label": "Skills", "href": "#skills"},
    ],
    # The outlined button on the right of the menu.
    "cta": {"label": "Get in touch", "href": "#contact"},
    # The phone menu repeats the links above and adds this one at the end.
    "mobile_extra": {"label": "Contact", "href": "#contact"},
}

# ---------------------------------------------------------------------------
# HERO  --  the full-screen opening panel
# ---------------------------------------------------------------------------

HERO = {
    "badge": "Available for AI engineering work",
    "name": "Daniel Cruz",
    "role": "AI Developer",
    "tags": ["RAG Pipelines", "Agentic Systems", "Cybersecurity"],
    "description_html": (
        "I build <strong>production-ready agentic systems</strong> that meet "
        "rigorous security and governance standards: RAG pipelines that ground "
        "LLMs in real documents, and multi-agent orchestration across "
        "<strong>LangChain, LangGraph, CrewAI, AutoGen and BeeAI</strong>, "
        "backed by hands-on cybersecurity training."
    ),
    "primary_button": {"label": "View credentials", "href": "#credentials"},
    "ghost_button": {"label": "Contact me", "href": "#contact"},
}

# The four counters under the hero. They count up from zero when the page loads.
# "plus" adds a "+" after the number.
STATS = [
    {"value": 11, "label": "Certifications", "plus": False},
    {"value": 10, "label": "IBM Courses", "plus": False},
    {"value": 8, "label": "Frameworks", "plus": True},
    {"value": 5, "label": "Yrs Production Exp.", "plus": True},
]

# The strip of scrolling words under the hero.
MARQUEE = [
    "LangChain",
    "LangGraph",
    "CrewAI",
    "AutoGen",
    "BeeAI",
    "MCP",
    "RAG Pipelines",
    "Vector Databases",
    "Python",
    "Cybersecurity",
]

# ---------------------------------------------------------------------------
# ABOUT
# ---------------------------------------------------------------------------

ABOUT = {
    "kicker": "About",
    "title_html": "From production floors<br>to production AI.",
    "paragraphs_html": [
        "I'm an AI developer based in <strong>Montreal, Canada</strong>, "
        "focused on the security and governance of agentic systems and RAG "
        "pipelines.",

        "Before AI, I spent <strong>five years as a technical designer</strong> "
        "managing large-scale production for clients in banking, real estate, "
        "retail and recreation. It was an environment where deadlines are hard, "
        "documentation must be exact, and mistakes are expensive. That critical, "
        "deadline-driven thinking now drives how I design and ship AI systems.",
    ],
    # Short lines with a green check mark beside them.
    "points": [
        "RAG pipelines that ground LLM answers in real, verifiable documents",
        "Multi-agent orchestration: planning, tool calling and state across steps",
        "Threat modelling, access control and data handling for systems touching "
        "production data",
    ],
}

# The bordered card on the right of the About section.
EXPERIENCE = {
    "role": "Technical Designer",
    "org": "Montreal Neon Signs · 5 years",
    "bullets": [
        "End-to-end oversight of the client technical database and production "
        "documentation systems",
        "Led a team of 2 drafters through high-volume production deadlines",
        "Designed structural and anchoring solutions for large-format signage "
        "installations",
        "2D drawings and 3D models for engineering approval and municipal "
        "permitting",
        "Managed material budgets and cross-team collaboration across concurrent "
        "projects",
    ],
}

# ---------------------------------------------------------------------------
# PROJECTS  --  the project cards. Each card opens its own page in Projects/.
# ---------------------------------------------------------------------------

PROJECTS_SECTION = {
    "kicker": "Projects",
    "title_html": "The projects I've built.",
    "subtitle": (
        "Each project opens an interactive walkthrough of how it works. "
        "On a computer, hover a card to watch it run."
    ),
}

# To add a project: copy one block, paste it below, change the values, and put
# its page in the Projects/ folder.
#
#   "page"     the project's own page (file names with spaces are fine)
#   "preview"  optional: what the hover preview loads; defaults to "page"
#   "accent"   the card's glow color, as a hex code
#   "icon"     optional: an image shown on the card cover; without one the
#              cover shows the project's initials
#   "category" groups projects for the filter buttons, which appear on their
#              own once there are 3+ projects in 2+ categories
#   "featured" True gives the card a whole row (use it on one project). It only
#              applies when the other projects pair up evenly, two per row;
#              otherwise it looks like the other cards
#   "metrics"  optional: up to 3 (value, label) pairs shown on the card
#   "features" optional: short feature names listed beside the metrics
PROJECTS = [
    {
        "title": "Desktop Manager",
        "tagline": "Your desktop icons, back where they belong on every monitor setup.",
        "description": (
            "A Windows tray app that saves a desktop icon layout for every display "
            "setup and restores it when you dock, undock or wake. It identifies "
            "monitors by EDID serial, maps layouts across resolutions, and adds "
            "zones, notes and widgets that never cover an icon."
        ),
        "page": "Projects/Desktop Manager.html",
        "preview": "Projects/Desktop Manager.html#preview",
        "icon": "Projects/assets/desktop-manager/app-icon-256.png",
        "accent": "#2F6B9A",
        "category": "Desktop app",
        "status": "In development",
        "year": "2026",
        "stack": ["C#", ".NET 10", "WPF", "Win32 interop", "xUnit"],
        "metrics": [("8", "widgets")],
        "features": ["Auto-restore", "Layout editor", "Autosave history",
                     "Always on Top", "Text Extractor"],
        "featured": True,
    },
    {
        "title": "Tailored Cleaner",
        "tagline": "Seven AI agents that tailor a CV and cover letter to a job post.",
        "description": (
            "A BeeAI multi-agent pipeline that reads the job and the CV, scores the "
            "match and stops before spending tokens on a weak fit, edits both "
            "documents, checks them in a validation loop, and exports PDFs. Every "
            "agent runs on an OpenRouter model chain with fallbacks."
        ),
        "page": "Projects/Tailored Cleaner.html",
        "preview": "Projects/Tailored Cleaner.html#preview",
        "icon": "Projects/assets/Tailored Cleaner/Tailored Cleaner.jpg",
        "accent": "#D9A07E",
        "category": "AI agents",
        "status": "Working prototype",
        "year": "2026",
        "stack": ["Python", "BeeAI", "OpenRouter", "Multi-agent"],
        "metrics": [("7", "agents")],
        "features": ["Cost gate", "Self-checking drafts", "Keeps your CV layout", "PDF export"],
    },
]

# ---------------------------------------------------------------------------
# CREDENTIALS  --  the two big certificate cards
# ---------------------------------------------------------------------------

CREDENTIALS_SECTION = {
    "kicker": "Credentials",
    "title_html": "Two pillars: agentic AI<br>and security.",
    "subtitle": (
        "Every credential on this page is independently verifiable. Coursera "
        "codes resolve at coursera.org/verify."
    ),
}

# "tags" become the small pills. Use "style": "blue" for the lighter pill.
# "link" is optional: it makes the whole card open that page.
CREDENTIALS = [
    {
        "image": "certs/ibm-cert.png",
        "alt": "IBM RAG and Agentic AI Professional Certificate",
        "tags": [
            {"label": "Professional Certificate"},
            {"label": "10 Courses", "style": "blue"},
        ],
        "title": "IBM RAG & Agentic AI Professional Certificate",
        "description": (
            "Ten courses on retrieval-augmented generation and autonomous "
            "agents: retrieval pipelines over vector databases, multi-step "
            "reasoning with LangChain and LangGraph, multi-agent architectures "
            "in CrewAI, AutoGen and BeeAI, and tool access through MCP."
        ),
        "issuer": "IBM Skills Network · Aug 2026",
        "code": "RT4C10Z9PPED",
        # Clicking the card opens the courses page (COURSES_PAGE below).
        "link": "ibm-courses.html",
        "link_label": "View the 9 courses",
    },
    {
        "image": "certs/cybersecurity.png",
        "alt": "Certificate in Cybersecurity Proficiency, Concordia University",
        "tags": [
            {"label": "University Certificate"},
            {"label": "Security", "style": "blue"},
        ],
        "title": "Certificate in Cybersecurity Proficiency",
        "description": (
            "Network and system security, threat and vulnerability assessment, "
            "cryptography, access control and incident response, applied to "
            "threat modelling and data handling for retrieval and agent systems "
            "that touch production data."
        ),
        "issuer": "Concordia University · Jun 2026",
        "code": "Montreal, CA",
    },
]

# ---------------------------------------------------------------------------
# COURSES  --  these live on their own page, opened from the IBM certificate
# card above. The page's heading, picture and code come from the credential
# whose "link" matches "file" below.
# ---------------------------------------------------------------------------

COURSES_PAGE = {
    "file": "ibm-courses.html",
    "title": "IBM Courses | DanielC Portfolio",
    "description": (
        "The nine verifiable courses behind Daniel Cruz's IBM RAG and Agentic AI "
        "Professional Certificate."
    ),
    "back_label": "Back to portfolio",
}

COURSES_SECTION = {
    "kicker": "Coursework",
    "title_html": "Nine certified courses,<br>one coherent stack.",
}

# The filter buttons. "key" must match a course "category" below.
# The "all" key is special: it shows everything.
COURSE_FILTERS = [
    {"key": "all", "label": "All"},
    {"key": "rag", "label": "RAG & Retrieval"},
    {"key": "agents", "label": "Agentic AI"},
    {"key": "genai", "label": "GenAI & Tools"},
]

# To add a course: copy one block, paste it below, change the values.
# "code" is the Coursera verification code; it becomes a link automatically.
COURSES = [
    {
        "title": "Develop Generative AI Applications",
        "category": "genai",
        "image": "certs/develop-genai.png",
        "date": "Apr 8, 2026",
        "code": "6957R7CTBQ8L",
    },
    {
        "title": "Build RAG Applications",
        "category": "rag",
        "image": "certs/build-rag.png",
        "date": "Apr 16, 2026",
        "code": "KLGI2BQ5XCW3",
    },
    {
        "title": "Vector Databases for RAG",
        "category": "rag",
        "image": "certs/vector-db.png",
        "date": "Apr 21, 2026",
        "code": "6JFJTO1O844Y",
    },
    {
        "title": "Advanced RAG with Vector Databases & Retrievers",
        "category": "rag",
        "image": "certs/advanced-rag.png",
        "date": "May 4, 2026",
        "code": "LNYDTW3UTZF5",
    },
    {
        "title": "Build Multimodal Generative AI Applications",
        "category": "genai",
        "image": "certs/multimodal.png",
        "date": "May 11, 2026",
        "code": "DX6GNES9TKKB",
    },
    {
        "title": "Fundamentals of Building AI Agents",
        "category": "agents",
        "image": "certs/agent-fundamentals.png",
        "date": "May 18, 2026",
        "code": "6QE81J6KXN0O",
    },
    {
        "title": "Agentic AI with LangChain & LangGraph",
        "category": "agents",
        "image": "certs/langchain-langgraph.png",
        "date": "May 25, 2026",
        "code": "MD2EC0CGX3WP",
    },
    {
        "title": "Agentic AI with LangGraph, CrewAI, AutoGen & BeeAI",
        "category": "agents",
        "image": "certs/multiframework.png",
        "date": "Jun 10, 2026",
        "code": "87PY5FGJOJ5C",
    },
    {
        "title": "Build AI Agents using MCP",
        "category": "agents",
        "image": "certs/mcp.png",
        "date": "Jul 28, 2026",
        "code": "OYADP9GDQPDE",
    },
]

# ---------------------------------------------------------------------------
# SKILLS  --  capability cards, then the stack grid
# ---------------------------------------------------------------------------

SKILLS_SECTION = {
    "kicker": "Capabilities",
    "title_html": "What the certificates attest.",
    "subtitle": "Six capabilities certified by IBM, built on a named stack.",
    "stack_kicker": "The stack behind them",
}

# Numbered automatically (/ 01, / 02, ...) in the order listed here.
CAPABILITIES = [
    {
        "title": "Prompting & Function Calling",
        "description": "Design effective prompts and implement function calling "
                       "against live APIs.",
    },
    {
        "title": "Reasoning Workflows",
        "description": "Orchestrate complex multi-step reasoning workflows with "
                       "tools like LangChain.",
    },
    {
        "title": "Autonomous Agents",
        "description": "Build autonomous and collaborative agents using memory, "
                       "feedback and chaining.",
    },
    {
        "title": "System Integration",
        "description": "Integrate APIs, tools and multi-step reasoning into "
                       "flexible, testable systems.",
    },
    {
        "title": "Multi-Agent Architecture",
        "description": "Design multi-agent architectures with CrewAI and "
                       "LangGraph.",
    },
    {
        "title": "Retrieval Pipelines",
        "description": "Build retrieval pipelines on vector databases and "
                       "advanced retrievers.",
    },
]

STACK = [
    {"name": "LangChain", "role": "Reasoning workflow orchestration"},
    {"name": "LangGraph", "role": "Stateful agent graphs"},
    {"name": "CrewAI", "role": "Multi-agent teams"},
    {"name": "AutoGen", "role": "Conversational agent patterns"},
    {"name": "BeeAI", "role": "Framework interoperability"},
    {"name": "MCP", "role": "Tool and data connection"},
    {"name": "Vector DBs", "role": "Embeddings and retrievers"},
    {"name": "Python", "role": "Implementation language"},
]

# ---------------------------------------------------------------------------
# CONTACT and FOOTER
# ---------------------------------------------------------------------------

CONTACT = {
    "kicker": "Contact",
    # The second half is printed in the green gradient.
    "title": "Let's build something",
    "title_highlight": "secure & intelligent.",
    "subtitle": (
        "Open to AI engineering roles and collaborations. Every credential "
        "above is verifiable, and if you have a question about my background, "
        "the assistant in the corner answers from it directly."
    ),
    "email": "danielcruzcastro30@gmail.com",
    "linkedin": "https://linkedin.com/in/daniel-cruz-0bab18224",
    "linkedin_label": "LinkedIn",
    "verify_note_html": (
        'Every Coursera code resolves at '
        '<a href="https://coursera.org/verify" target="_blank" rel="noopener">'
        'coursera.org/verify</a>'
    ),
}

FOOTER = {
    "copy": "© 2026 Daniel Cruz · Built with an unreasonable attention to detail.",
    "links": [
        {"label": "Email", "href": "mailto:danielcruzcastro30@gmail.com"},
        {"label": "LinkedIn", "href": "https://linkedin.com/in/daniel-cruz-0bab18224"},
        {"label": "Verify", "href": "https://coursera.org/verify"},
    ],
}

# ---------------------------------------------------------------------------
# ASSISTANT  --  the chatbot in the bottom-right corner
#
# "prompt" below is the system prompt: everything the assistant knows and the
# rules it answers by. Write it as ordinary prose. It is written out to
# assistant-config.js by build.py, so quotes and apostrophes are safe here.
# ---------------------------------------------------------------------------

ASSISTANT = {
    "name": "Daniel's Assistant",
    "status": "online - AI powered ✨",
    "greeting": (
        "Hi! I answer questions about Daniel's credentials, experience and "
        "stack. Everything comes straight from this portfolio."
    ),
    # The popup bubble that invites visitors to open the chat.
    "nudge_html": "Have any questions? <strong>Ask my AI assistant</strong>",
    # The starter questions shown when the chat is opened.
    "suggestions": [
        "What is Daniel's tech stack",
        "Which agent frameworks has he worked with?",
        "How does the cybersecurity certificate apply to AI work?",
    ],
    "prompt": """You answer questions about Daniel Cruz, an AI Developer based in Laval, on behalf of his credentials portfolio deck and work experience achievements. Be concise, factual and professional. If asked a question you do not have the answer to, explain that you cannot provide the answer since you do not have the information needed, and recommend sending Daniel an email instead.

POSITIONING: Focused on the security and governance of agentic systems and RAG pipelines. Five years managing large-scale production for banking, real estate, retail, and recreational clients as a technical designer built the critical, deadline-driven thinking now applied to RAG applications and agentic systems.

CREDENTIALS (11 total):
- IBM RAG and Agentic AI Professional Certificate (IBM Skills Network via Coursera, awarded Aug 20 2026, code RT4C10Z9PPED) — ten courses.
- Certificate in Cybersecurity Proficiency (Concordia University, Continuing Education, Montreal, Jun 30 2026).
Courses within the IBM certificate: Develop Generative AI Applications: Get Started (Apr 8 2026, 6957R7CTBQ8L); Build RAG Applications: Get Started (Apr 16 2026, KLGI2BQ5XCW3); Vector Databases for RAG: An Introduction (Apr 21 2026, 6JFJTO1O844Y); Advanced RAG with Vector Databases and Retrievers (May 4 2026, LNYDTW3UTZF5); Build Multimodal Generative AI Applications (May 11 2026, DX6GNES9TKKB); Fundamentals of Building AI Agents (May 18 2026, 6QE81J6KXN0O); Agentic AI with LangChain and LangGraph (May 25 2026, MD2EC0CGX3WP); Agentic AI with LangGraph, CrewAI, AutoGen and BeeAI (Jun 10 2026, 87PY5FGJOJ5C); Build AI Agents using MCP (Jul 28 2026, OYADP9GDQPDE).

CERTIFIED CAPABILITIES (IBM attestation): design effective prompts and implement function calling; orchestrate complex reasoning workflows with tools like LangChain; build autonomous and collaborative agents using memory, feedback and chaining; integrate APIs, tools and multi-step reasoning into flexible systems; design multi-agent architectures with CrewAI and LangGraph; build retrieval pipelines on vector databases and retrievers.

STACK: LangChain, LangGraph, CrewAI, AutoGen, BeeAI, MCP, vector databases and retrievers, RAG pipelines, Python.

CODING LANGUAGES: mainly Python, some experience with JSON and JavaScript.

CYBERSECURITY: network and system security, threat and vulnerability assessment, cryptography, access control, incident response, governance and risk — applied to threat modelling, data handling and access control for retrieval and agent systems that touch production data.

CONTACT: danielcruzcastro30@gmail.com · linkedin.com/in/daniel-cruz-0bab18224. All Coursera codes resolve at coursera.org/verify.

FORMAT: reply in plain prose sentences only. Never use markdown syntax — no asterisks for bold or italics, no headings, no hyphen or bullet lists, no code fences. Keep answers under about 60 words.

Work experience achievements: At Montreal Neon Signs Daniel assumed end-to-end oversight of the company's client technical database, ensuring the accurate development and maintenance of production documentation systems; he also led a team of 2 drafters to meet high-volume production deadlines and maintain large-scale client project files, while designing structural systems and anchoring solutions for large-format signage installations. He also managed material budgets and cross-team collaboration with production and installation across multiple concurrent projects, and developed 2D technical drawings and 3D models for engineering approval and municipal permitting, ensuring structural safety and code compliance for signage installation processes.""",
}
