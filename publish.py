#!/usr/bin/env python3
"""
fastmail-blog/publish.py
Static blog publisher → Fastmail WebDAV

Usage:
    python publish.py post.md              # publish one post
    python publish.py --rebuild-index      # regenerate all index pages
    python publish.py --list               # list published posts
    python publish.py --delete slug        # delete a post

Authentication: App Password from Fastmail → Settings → Privacy & Security → Manage app passwords
WebDAV URL:     Check Fastmail → Settings → Files & Storage
"""

import argparse
import os
import sys
import json
import re
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
    import markdown
    import yaml
except ImportError:
    print("Missing dependencies. Run: pip install requests markdown pyyaml")
    sys.exit(1)

# ─────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────

CONFIG_FILE = Path(".blog-config.json")

DEFAULT_CONFIG = {
    "webdav_base_url": "https://myfiles.fastmail.com/",
    "webdav_username": "",
    "webdav_app_password": "",
    "blog_path": "blog/",
    "site_title": "My Blog",
    "site_description": "",
    "author": "",
    "base_url": "https://yourdomain.com/blog/",
    "posts_per_page": 10,
}


def load_config() -> dict:
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            cfg = json.load(f)
        for k, v in DEFAULT_CONFIG.items():
            cfg.setdefault(k, v)
        return cfg
    print("No .blog-config.json found. Creating one — please fill in your credentials.")
    with open(CONFIG_FILE, "w") as f:
        json.dump(DEFAULT_CONFIG, f, indent=2)
    print(f"Edit {CONFIG_FILE} and run again.")
    sys.exit(0)


# ─────────────────────────────────────────
# Markdown → frontmatter + HTML
# ─────────────────────────────────────────

def parse_markdown(path: Path) -> tuple[dict, str]:
    raw = path.read_text(encoding="utf-8")
    frontmatter = {}
    body = raw
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", raw, re.DOTALL)
    if fm_match:
        try:
            frontmatter = yaml.safe_load(fm_match.group(1)) or {}
        except yaml.YAMLError as e:
            print(f"Warning: invalid YAML frontmatter — {e}")
        body = raw[fm_match.end():]

    extracted = extract_date_from_body(body)
    if extracted:
        frontmatter["date"] = extracted

    md = markdown.Markdown(
        extensions=["fenced_code", "codehilite", "tables", "toc", "footnotes", "attr_list"],
        extension_configs={
            "codehilite": {"css_class": "highlight", "guess_lang": False},
            "toc": {"permalink": True},
        },
    )
    return frontmatter, md.convert(body)


def extract_date_from_body(body: str) -> str | None:
    """Extract date from inline patterns like _ 20 May, 2024 _ in the markdown body."""
    match = re.search(r"_\s*((?:\d{1,2}\s+\w+|\w+\s+\d{1,2}),?\s+\d{4})\s*_", body)
    if not match:
        return None
    raw = match.group(1).strip()
    for fmt in ("%d %b, %Y", "%d %b %Y", "%b %d, %Y", "%b %d %Y",
                "%d %B, %Y", "%d %B %Y", "%B %d, %Y", "%B %d %Y"):
        try:
            return datetime.strptime(raw, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return re.sub(r"-+", "-", text)


def resolve_meta(frontmatter: dict, source_path: Path) -> dict:
    meta = dict(frontmatter)
    meta.setdefault("title", source_path.stem.replace("-", " ").title())
    meta.setdefault("date", datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    if not isinstance(meta["date"], str):
        meta["date"] = meta["date"].strftime("%Y-%m-%d")
    meta.setdefault("slug", slugify(meta["title"]))
    meta.setdefault("description", "")
    meta.setdefault("tags", [])
    if isinstance(meta["tags"], str):
        meta["tags"] = [t.strip() for t in meta["tags"].split(",")]
    return meta


# ─────────────────────────────────────────
# CSS
# ─────────────────────────────────────────

CSS = """
    @import url('https://fonts.googleapis.com/css2?family=Josefin+Sans:wght@600;700&family=Lora:ital,wght@0,400;0,500;1,400&family=JetBrains+Mono:wght@400&display=swap');

    :root {
      --bg:           #1a2332;
      --surface:      #1f2b3e;
      --border:       #2a3d56;
      --text:         #f1faee;
      --muted:        #a8dadc;
      --accent:       #2d8b8b;
      --accent-hover: #a8dadc;
      --code-bg:      #141c2b;
      --tag-bg:       #1e2d42;
      --font-display: 'Josefin Sans', system-ui, sans-serif;
      --font-body:    'Lora', Georgia, serif;
      --font-mono:    'JetBrains Mono', monospace;
      --font-ui:      'Josefin Sans', system-ui, sans-serif;
      --max-w:        720px;
      --radius:       3px;
    }

    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    html { font-size: 18px; scroll-behavior: smooth; }

    body {
      background: var(--bg);
      color: var(--text);
      font-family: var(--font-body);
      line-height: 1.8;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    /* ── Header ──────────────────────────── */
    .site-header {
      padding: 2rem 2.5rem 1.75rem;
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 1rem;
    }

    .site-header-left { flex: 1; }

    .site-name {
      font-family: var(--font-display);
      font-weight: 700;
      font-size: 1.2rem;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--accent-hover);
      text-decoration: none;
      display: block;
      line-height: 1;
      margin-bottom: 0.35rem;
    }

    .site-name:hover { color: #ffffff; }

    .site-tagline {
      font-family: var(--font-body);
      font-style: italic;
      font-size: 0.82rem;
      color: var(--muted);
      opacity: 0.8;
    }

    .site-search-link {
      font-family: var(--font-ui);
      font-size: 0.68rem;
      color: var(--muted);
      text-decoration: none;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      padding: 0.4em 0.9em;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      white-space: nowrap;
      align-self: center;
      transition: color 0.2s, border-color 0.2s;
    }

    .site-search-link:hover {
      color: var(--accent-hover);
      border-color: var(--accent);
    }

    /* ── Main ───────────────────────────── */
    main {
      flex: 1;
      max-width: var(--max-w);
      width: 100%;
      margin: 0 auto;
      padding: 3.5rem 2.5rem 5rem;
    }

    /* ── Post list ──────────────────────── */
    .post-list { list-style: none; }

    .post-list li {
      padding: 1.75rem 0;
      border-bottom: 1px solid var(--border);
    }

    .post-list li:first-child { border-top: 1px solid var(--border); }

    .post-list .post-title {
      font-family: var(--font-display);
      font-weight: 700;
      font-size: 1.05rem;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      line-height: 1.4;
      color: var(--text);
      text-decoration: none;
      display: block;
      margin-bottom: 0.45rem;
      transition: color 0.2s;
    }

    .post-list .post-title:hover { color: var(--accent-hover); }

    .post-list .meta {
      font-family: var(--font-ui);
      font-size: 0.67rem;
      color: var(--accent);
      letter-spacing: 0.1em;
      text-transform: uppercase;
      display: flex;
      gap: 1rem;
      align-items: center;
      flex-wrap: wrap;
      margin-bottom: 0.5rem;
    }

    .post-list .desc {
      font-family: var(--font-body);
      font-style: italic;
      font-size: 0.9rem;
      color: var(--muted);
      line-height: 1.55;
      opacity: 0.85;
    }

    /* ── Tags ──────────────────────────── */
    .tag {
      background: var(--tag-bg);
      color: var(--accent);
      font-family: var(--font-ui);
      font-size: 0.6rem;
      padding: 0.2em 0.65em;
      border-radius: var(--radius);
      letter-spacing: 0.1em;
      text-transform: uppercase;
      border: 1px solid var(--border);
    }

    /* ── Pagination ─────────────────────── */
    .pagination {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding-top: 2.5rem;
      font-family: var(--font-ui);
      font-size: 0.72rem;
      letter-spacing: 0.06em;
    }

    .pagination a {
      color: var(--muted);
      text-decoration: none;
      padding: 0.4em 0.9em;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      text-transform: uppercase;
      transition: color 0.2s, border-color 0.2s;
    }

    .pagination a:hover {
      color: var(--accent-hover);
      border-color: var(--accent);
    }

    .pagination .pages { display: flex; gap: 0.3rem; }

    .pagination .pages a,
    .pagination .pages span {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 2rem;
      height: 2rem;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      text-decoration: none;
      color: var(--muted);
      transition: color 0.2s, border-color 0.2s;
    }

    .pagination .pages a:hover {
      color: var(--accent-hover);
      border-color: var(--accent);
    }

    .pagination .pages .current {
      border-color: var(--accent);
      color: var(--accent-hover);
      font-weight: 600;
    }

    /* ── Post article ───────────────────── */
    .post-header {
      margin-bottom: 3rem;
      padding-bottom: 2rem;
      border-bottom: 1px solid var(--border);
    }

    .post-header h1 {
      font-family: var(--font-display);
      font-weight: 700;
      font-size: 2rem;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      line-height: 1.2;
      margin-bottom: 1rem;
      color: var(--text);
    }

    .post-meta {
      display: flex;
      gap: 0.75rem;
      align-items: center;
      flex-wrap: wrap;
      font-family: var(--font-ui);
      font-size: 0.67rem;
      color: var(--accent);
      letter-spacing: 0.1em;
      text-transform: uppercase;
    }

    /* ── Prose ──────────────────────────── */
    .post-body { max-width: 68ch; }

    .post-body h2, .post-body h3, .post-body h4 {
      font-family: var(--font-display);
      margin: 2.5rem 0 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--text);
    }

    .post-body h2 { font-size: 1.25rem; font-weight: 700; }
    .post-body h3 { font-size: 1rem; font-weight: 600; color: var(--muted); }
    .post-body h4 { font-size: 0.72rem; color: var(--accent); letter-spacing: 0.12em; }

    .post-body p { margin: 1.2rem 0; }

    .post-body a {
      color: var(--accent-hover);
      text-decoration: underline;
      text-decoration-color: var(--accent);
      text-underline-offset: 3px;
      transition: color 0.2s;
    }

    .post-body a:hover { color: #ffffff; }

    .post-body ul, .post-body ol { padding-left: 1.5rem; margin: 1.2rem 0; }
    .post-body li { margin: 0.35rem 0; }

    .post-body blockquote {
      border-left: 2px solid var(--accent);
      padding: 0.5rem 0 0.5rem 1.5rem;
      margin: 2rem 0;
      color: var(--muted);
      font-style: italic;
      font-size: 1.05rem;
    }

    .post-body table {
      width: 100%;
      border-collapse: collapse;
      font-family: var(--font-ui);
      font-size: 0.78rem;
      margin: 2rem 0;
    }

    .post-body th, .post-body td {
      border: 1px solid var(--border);
      padding: 0.55rem 0.85rem;
      text-align: left;
    }

    .post-body th {
      background: var(--surface);
      font-weight: 700;
      letter-spacing: 0.08em;
      font-size: 0.67rem;
      text-transform: uppercase;
      color: var(--accent);
    }

    .post-body tr:nth-child(even) td { background: var(--surface); }

    .post-body code {
      font-family: var(--font-mono);
      font-size: 0.78em;
      background: var(--code-bg);
      padding: 0.12em 0.45em;
      border-radius: var(--radius);
      color: var(--accent-hover);
    }

    .post-body pre {
      background: var(--code-bg);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 1.25rem 1.5rem;
      overflow-x: auto;
      margin: 2rem 0;
    }

    .post-body pre code {
      background: none;
      padding: 0;
      font-size: 0.8rem;
      line-height: 1.65;
      color: var(--text);
    }

    .post-body img { max-width: 100%; border-radius: var(--radius); margin: 2rem 0; }

    .post-body hr {
      border: none;
      border-top: 1px solid var(--border);
      margin: 3rem 0;
    }

    /* ── Post nav ───────────────────────── */
    .post-nav {
      margin-top: 3.5rem;
      padding-top: 1.5rem;
      border-top: 1px solid var(--border);
      font-family: var(--font-ui);
      font-size: 0.7rem;
      letter-spacing: 0.1em;
      text-transform: uppercase;
    }

    .post-nav a { color: var(--accent); text-decoration: none; }
    .post-nav a:hover { color: var(--accent-hover); }

    /* ── Search page ─────────────────────── */
    .search-wrap { margin-bottom: 2.5rem; }

    .search-input {
      width: 100%;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      color: var(--text);
      font-family: var(--font-body);
      font-size: 1.05rem;
      padding: 0.7em 1em;
      outline: none;
      transition: border-color 0.2s;
    }

    .search-input:focus { border-color: var(--accent); }
    .search-input::placeholder { color: var(--muted); font-style: italic; opacity: 0.6; }

    .search-meta {
      font-family: var(--font-ui);
      font-size: 0.67rem;
      color: var(--accent);
      margin-top: 0.75rem;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      min-height: 1.2em;
    }

    .search-results { list-style: none; }
    .search-results li { padding: 1.5rem 0; border-bottom: 1px solid var(--border); }
    .search-results li:first-child { border-top: 1px solid var(--border); }

    .search-results .post-title {
      font-family: var(--font-display);
      font-weight: 700;
      font-size: 1rem;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: var(--text);
      text-decoration: none;
      display: block;
      margin-bottom: 0.35rem;
    }

    .search-results .post-title:hover { color: var(--accent-hover); }

    .search-results .meta {
      font-family: var(--font-ui);
      font-size: 0.67rem;
      color: var(--accent);
      letter-spacing: 0.1em;
      text-transform: uppercase;
      margin-bottom: 0.4rem;
      display: flex;
      gap: 0.75rem;
      flex-wrap: wrap;
    }

    .search-results .desc {
      font-style: italic;
      font-size: 0.9rem;
      color: var(--muted);
      opacity: 0.85;
    }

    mark {
      background: transparent;
      color: var(--accent-hover);
      font-weight: 600;
    }

    .no-results {
      font-family: var(--font-ui);
      color: var(--muted);
      padding: 2rem 0;
      font-size: 0.8rem;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }

    /* ── Footer ─────────────────────────── */
    footer {
      border-top: 1px solid var(--border);
      padding: 1.5rem 2.5rem;
      font-family: var(--font-ui);
      font-size: 0.65rem;
      color: var(--accent);
      text-align: center;
      letter-spacing: 0.1em;
      text-transform: uppercase;
    }

    /* ── Responsive ─────────────────────── */
    @media (max-width: 600px) {
      html { font-size: 16px; }
      main { padding: 2rem 1.5rem 3.5rem; }
      .site-header { padding: 1.5rem; }
      .post-header h1 { font-size: 1.5rem; }
    }
"""

# ─────────────────────────────────────────
# HTML templates
# ─────────────────────────────────────────

POST_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} · {site_title}</title>
  <meta name="description" content="{description}" />
  <meta name="author" content="{author}" />
  <link rel="canonical" href="{canonical_url}" />
  <link rel="alternate" type="application/rss+xml" title="{site_title}" href="{base_url}feed.xml" />
  <style>{css}</style>
</head>
<body>
  <header class="site-header">
    <div class="site-header-left">
      <a href="{base_url}" class="site-name">{site_title}</a>
      {tagline_html}
    </div>
    <a href="{base_url}search/" class="site-search-link">⌕ Search</a>
  </header>

  <main>
    <article>
      <header class="post-header">
        <h1>{title}</h1>
        <div class="post-meta">
          <time datetime="{date}">{date_formatted}</time>
          {tags_html}
        </div>
      </header>
      <div class="post-body">
{body}
      </div>
    </article>
    <nav class="post-nav">
      <a href="{base_url}">← All posts</a>
    </nav>
  </main>

  <footer>
    <p>© {year} {author}</p>
  </footer>
</body>
</html>
"""

INDEX_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{page_title}</title>
  <meta name="description" content="{site_description}" />
  <link rel="alternate" type="application/rss+xml" title="{site_title}" href="{root_url}feed.xml" />
  <style>{css}</style>
</head>
<body>
  <header class="site-header">
    <div class="site-header-left">
      <a href="{root_url}" class="site-name">{site_title}</a>
      {tagline_html}
    </div>
    <a href="{root_url}search/" class="site-search-link">⌕ Search</a>
  </header>

  <main>
    <ol class="post-list" start="{list_start}">
{post_items}
    </ol>

    {pagination_html}
  </main>

  <footer>
    <p>© {year} {author}</p>
  </footer>
</body>
</html>
"""


# ─────────────────────────────────────────
# Render functions
# ─────────────────────────────────────────

def render_post(meta: dict, html_body: str, cfg: dict) -> str:
    date_obj = datetime.strptime(meta["date"], "%Y-%m-%d")
    date_formatted = date_obj.strftime("%B %d, %Y")
    year = datetime.now().year
    tags_html = " ".join(f'<span class="tag">{t}</span>' for t in meta["tags"])
    tagline_html = (
        f'<span class="site-tagline">{cfg["site_description"]}</span>'
        if cfg.get("site_description") else ""
    )
    return POST_TEMPLATE.format(
        title=meta["title"],
        site_title=cfg["site_title"],
        description=meta.get("description", ""),
        author=cfg["author"],
        base_url=cfg["base_url"],
        canonical_url=cfg["base_url"] + meta["slug"] + "/",
        date=meta["date"],
        date_formatted=date_formatted,
        tags_html=tags_html,
        tagline_html=tagline_html,
        body=html_body,
        year=year,
        css=CSS,
    )


def render_index_page(posts_page: list[dict], cfg: dict, page_num: int, total_pages: int) -> str:
    """Render one page of the index. page_num is 1-based."""
    year = datetime.now().year
    base = cfg["base_url"]
    per_page = cfg.get("posts_per_page", 10)

    tagline_html = (
        f'<span class="site-tagline">{cfg["site_description"]}</span>'
        if cfg.get("site_description") else ""
    )

    page_title = cfg["site_title"] if page_num == 1 else f'{cfg["site_title"]} — page {page_num}'

    # Post items
    items = []
    for p in posts_page:
        date_obj = datetime.strptime(p["date"], "%Y-%m-%d")
        date_fmt = date_obj.strftime("%b %d, %Y")
        tags_html = " ".join(f'<span class="tag">{t}</span>' for t in p.get("tags", []))
        desc_html = f'<p class="desc">{p["description"]}</p>' if p.get("description") else ""
        items.append(
            f'      <li>\n'
            f'        <a class="post-title" href="{base}{p["slug"]}/">{p["title"]}</a>\n'
            f'        <div class="meta"><time>{date_fmt}</time>{tags_html}</div>\n'
            f'        {desc_html}\n'
            f'      </li>'
        )

    # Pagination
    def page_url(n):
        return base if n == 1 else f"{base}page/{n}/"

    pagination_html = ""
    if total_pages > 1:
        prev_link = f'<a href="{page_url(page_num - 1)}">← Newer</a>' if page_num > 1 else '<span></span>'
        next_link = f'<a href="{page_url(page_num + 1)}">Older →</a>' if page_num < total_pages else '<span></span>'

        pages = []
        for n in range(1, total_pages + 1):
            if n == page_num:
                pages.append(f'<span class="current">{n}</span>')
            else:
                pages.append(f'<a href="{page_url(n)}">{n}</a>')

        pagination_html = (
            f'<nav class="pagination">'
            f'{prev_link}'
            f'<div class="pages">{"".join(pages)}</div>'
            f'{next_link}'
            f'</nav>'
        )

    list_start = (page_num - 1) * per_page + 1

    return INDEX_TEMPLATE.format(
        page_title=page_title,
        site_title=cfg["site_title"],
        site_description=cfg.get("site_description", ""),
        tagline_html=tagline_html,
        root_url=base,
        post_items="\n".join(items),
        pagination_html=pagination_html,
        list_start=list_start,
        year=year,
        author=cfg["author"],
        css=CSS,
    )


def render_all_index_pages(posts: list[dict], cfg: dict) -> list[tuple[int, str]]:
    """Return list of (page_num, html) for all pages."""
    per_page = cfg.get("posts_per_page", 10)
    total = len(posts)
    total_pages = max(1, -(-total // per_page))  # ceiling division
    pages = []
    for n in range(1, total_pages + 1):
        chunk = posts[(n - 1) * per_page : n * per_page]
        pages.append((n, render_index_page(chunk, cfg, n, total_pages)))
    return pages


# ─────────────────────────────────────────
# WebDAV client
# ─────────────────────────────────────────

class WebDAVClient:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url.rstrip("/") + "/"
        self.session = requests.Session()
        self.session.auth = (username, password)
        self.session.headers["User-Agent"] = "fastmail-blog/1.0"

    def _url(self, path: str) -> str:
        return self.base_url + path.lstrip("/")

    def mkcol(self, path: str) -> bool:
        r = self.session.request("MKCOL", self._url(path))
        return r.status_code in (201, 405)

    def put(self, path: str, content: str) -> bool:
        r = self.session.put(
            self._url(path),
            data=content.encode("utf-8"),
            headers={"Content-Type": "text/html; charset=utf-8"},
        )
        return r.status_code in (200, 201, 204)

    def delete(self, path: str) -> bool:
        r = self.session.delete(self._url(path))
        return r.status_code in (200, 204, 404)

    def test_connection(self) -> bool:
        try:
            r = self.session.request("OPTIONS", self.base_url, timeout=10)
            return r.status_code < 400
        except requests.RequestException as e:
            print(f"Connection error: {e}")
            return False


# ─────────────────────────────────────────
# Registry
# ─────────────────────────────────────────

REGISTRY_FILE = Path(".blog-posts.json")


def load_registry() -> list[dict]:
    if REGISTRY_FILE.exists():
        with open(REGISTRY_FILE) as f:
            return json.load(f)
    return []


def save_registry(posts: list[dict]):
    with open(REGISTRY_FILE, "w") as f:
        json.dump(posts, f, indent=2)


def upsert_post(posts: list[dict], meta: dict) -> list[dict]:
    posts = [p for p in posts if p["slug"] != meta["slug"]]
    posts.append({k: meta[k] for k in ("title", "date", "slug", "description", "tags")})
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def remove_post(posts: list[dict], slug: str) -> list[dict]:
    return [p for p in posts if p["slug"] != slug]


# ─────────────────────────────────────────
# Upload helpers
# ─────────────────────────────────────────


def render_search_page(cfg: dict) -> str:
    """Generate the static search.html page (JS fetches search.json at runtime)."""
    year = __import__('datetime').datetime.now().year
    base = cfg["base_url"]
    tagline_html = (
        f'<span class="site-tagline">{cfg["site_description"]}</span>'
        if cfg.get("site_description") else ""
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Search · {cfg["site_title"]}</title>
  <style>{CSS}</style>
</head>
<body>
  <header class="site-header">
    <div class="site-header-left">
      <a href="{base}" class="site-name">{cfg["site_title"]}</a>
      {tagline_html}
    </div>
    <a href="{base}" class="site-search-link">← All posts</a>
  </header>

  <main>
    <div class="search-wrap">
      <input
        id="q"
        class="search-input"
        type="search"
        placeholder="Search posts…"
        autofocus
        autocomplete="off"
      />
      <p class="search-meta" id="meta"></p>
    </div>
    <ul class="search-results" id="results"></ul>
  </main>

  <footer>
    <p>© {year} {cfg["author"]}</p>
  </footer>

  <script>
    const BASE = {json.dumps(base)};
    let INDEX = [];

    async function loadIndex() {{
      const r = await fetch(BASE + 'search.json?v=' + Date.now());
      INDEX = await r.json();
      const q = new URLSearchParams(location.search).get('q') || '';
      if (q) {{ document.getElementById('q').value = q; search(q); }}
    }}

    function esc(s) {{
      return s.replace(/[&<>"']/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));
    }}

    function highlight(text, query) {{
      if (!query || !text) return esc(text || '');
      const re = new RegExp('(' + query.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&') + ')', 'gi');
      return esc(text).replace(re, '<mark>$1</mark>');
    }}

    function search(raw) {{
      const q = raw.trim().toLowerCase();
      const meta = document.getElementById('meta');
      const list = document.getElementById('results');

      if (!q) {{
        meta.textContent = '';
        list.innerHTML = '';
        return;
      }}

      const tokens = q.split(/[\\s]+/);
      const hits = INDEX.filter(p => {{
        const hay = [p.title, p.description, ...(p.tags || [])].join(' ').toLowerCase();
        return tokens.every(t => hay.includes(t));
      }});

      meta.textContent = hits.length
        ? hits.length + ' result' + (hits.length !== 1 ? 's' : '')
        : '';

      if (!hits.length) {{
        list.innerHTML = '<li class="no-results">No posts found.</li>';
        return;
      }}

      list.innerHTML = hits.map(p => {{
        const date = new Date(p.date + 'T00:00:00').toLocaleDateString('en-US', {{year:'numeric',month:'short',day:'numeric'}});
        const tags = (p.tags || []).map(t => `<span class="tag">${{esc(t)}}</span>`).join('');
        const desc = p.description ? `<p class="desc">${{highlight(p.description, raw.trim())}}</p>` : '';
        return `<li>
          <a class="post-title" href="${{BASE}}${{p.slug}}/">${{highlight(p.title, raw.trim())}}</a>
          <div class="meta"><time>${{date}}</time>${{tags}}</div>
          ${{desc}}
        </li>`;
      }}).join('');
    }}

    document.getElementById('q').addEventListener('input', e => search(e.target.value));
    loadIndex();
  </script>
</body>
</html>"""

def render_rss(posts: list[dict], cfg: dict) -> str:
    from email.utils import format_datetime
    base = cfg["base_url"]
    items = []
    for p in posts:
        pub_date = format_datetime(datetime.strptime(p["date"], "%Y-%m-%d").replace(tzinfo=timezone.utc))
        from html import escape
        items.append(
            f"  <item>\n"
            f"    <title>{escape(p['title'])}</title>\n"
            f"    <link>{base}{p['slug']}/</link>\n"
            f"    <guid isPermaLink=\"true\">{base}{p['slug']}/</guid>\n"
            f"    <pubDate>{pub_date}</pubDate>\n"
            f"    <description>{escape(p.get('description', ''))}</description>\n"
            f"  </item>"
        )
    last_build = format_datetime(datetime.now(timezone.utc))
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
        "<channel>\n"
        f"  <title>{escape(cfg['site_title'])}</title>\n"
        f"  <link>{base}</link>\n"
        f"  <description>{escape(cfg.get('site_description', ''))}</description>\n"
        f"  <lastBuildDate>{last_build}</lastBuildDate>\n"
        f'  <atom:link href="{base}feed.xml" rel="self" type="application/rss+xml" />\n'
        + "\n".join(items)
        + "\n</channel>\n</rss>\n"
    )


def upload_index(dav: WebDAVClient, posts: list[dict], cfg: dict):
    """Upload all paginated index pages, search.json and search.html to WebDAV."""
    blog_path = cfg["blog_path"].strip("/")
    pages = render_all_index_pages(posts, cfg)
    total = len(pages)

    # Paginated index pages
    if total > 1:
        dav.mkcol(f"{blog_path}/page")

    for page_num, html in pages:
        if page_num == 1:
            path = f"{blog_path}/index.html"
        else:
            dav.mkcol(f"{blog_path}/page/{page_num}")
            path = f"{blog_path}/page/{page_num}/index.html"
        ok = dav.put(path, html)
        status = "✓" if ok else "✗"
        print(f"  {status} Page {page_num}/{total}")

    # Search index (JSON)
    search_data = json.dumps(
        [{"title": p["title"], "slug": p["slug"], "date": p["date"],
          "description": p.get("description", ""), "tags": p.get("tags", [])}
         for p in posts],
        ensure_ascii=False
    )
    dav.session.put(
        dav._url(f"{blog_path}/search.json"),
        data=search_data.encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
    )

    # Search page (HTML)
    dav.mkcol(f"{blog_path}/search")
    search_html = render_search_page(cfg)
    ok = dav.put(f"{blog_path}/search/index.html", search_html)
    status = "✓" if ok else "✗"
    print(f"  {status} Search page")

    # RSS feed
    rss_xml = render_rss(posts, cfg)
    ok = dav.session.put(
        dav._url(f"{blog_path}/feed.xml"),
        data=rss_xml.encode("utf-8"),
        headers={"Content-Type": "application/rss+xml; charset=utf-8"},
    ).status_code in (200, 201, 204)
    status = "✓" if ok else "✗"
    print(f"  {status} RSS feed → {cfg['base_url']}feed.xml")


# ─────────────────────────────────────────
# Commands
# ─────────────────────────────────────────

def cmd_publish(source: Path, cfg: dict, no_index: bool = False):
    if not source.exists():
        print(f"File not found: {source}")
        sys.exit(1)

    print(f"Parsing {source}...")
    frontmatter, html_body = parse_markdown(source)
    meta = resolve_meta(frontmatter, source)

    _body_date = extract_date_from_body(source.read_text(encoding="utf-8"))
    date_source = "(from body)" if _body_date else "(from frontmatter)" if frontmatter.get("date") else "(today)"
    print(f"  Title : {meta['title']}")
    print(f"  Slug  : {meta['slug']}")
    print(f"  Date  : {meta['date']}  {date_source}")
    print(f"  Tags  : {', '.join(meta['tags']) or '—'}")

    post_html = render_post(meta, html_body, cfg)

    dav = WebDAVClient(cfg["webdav_base_url"], cfg["webdav_username"], cfg["webdav_app_password"])

    print("Testing WebDAV connection...")
    if not dav.test_connection():
        print("Could not connect. Check webdav_base_url and credentials in .blog-config.json")
        sys.exit(1)

    blog_path = cfg["blog_path"].strip("/")
    slug = meta["slug"]

    dav.mkcol(blog_path)
    dav.mkcol(f"{blog_path}/{slug}")

    print("Uploading post...")
    ok = dav.put(f"{blog_path}/{slug}/index.html", post_html)
    if not ok:
        print("Upload failed.")
        sys.exit(1)

    posts = load_registry()
    posts = upsert_post(posts, meta)
    save_registry(posts)

    if no_index:
        print(f"\n✓ Published → {cfg['base_url']}{slug}/  (index skipped)")
    else:
        print("Uploading index pages...")
        upload_index(dav, posts, cfg)
        print(f"\n✓ Published → {cfg['base_url']}{slug}/")


def _ascii_slug(s: str) -> str:
    import unicodedata
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s.lower()


def cmd_fix_dates():
    posts = load_registry()
    scan_dirs = [Path("posts_antigos"), Path("posts_novos")]

    # build lookup: exact stem + ascii-normalized stem → file
    slug_to_file: dict[str, Path] = {}
    for d in scan_dirs:
        if d.exists():
            for f in d.glob("*.md"):
                slug_to_file[f.stem] = f
                slug_to_file[_ascii_slug(f.stem)] = f

    fixed = 0
    for post in posts:
        slug = post["slug"]
        md_file = (slug_to_file.get(slug)
                   or slug_to_file.get(_ascii_slug(slug)))
        if md_file is None:
            for d in scan_dirs:
                candidate = d / f"{slug}.md"
                if candidate.exists():
                    md_file = candidate
                    break
        if md_file is None:
            continue
        raw = md_file.read_text(encoding="utf-8")
        fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", raw, re.DOTALL)
        body = raw[fm_match.end():] if fm_match else raw
        extracted = extract_date_from_body(body)
        if extracted and extracted != post["date"]:
            print(f"  {slug}: {post['date']} → {extracted}")
            post["date"] = extracted
            fixed += 1

    posts.sort(key=lambda p: p["date"], reverse=True)
    save_registry(posts)
    print(f"\n✓ Fixed {fixed} date(s). Registry saved.")


def cmd_rebuild_index(cfg: dict):
    posts = load_registry()
    if not posts:
        print("No posts in registry. Publish something first.")
        return
    dav = WebDAVClient(cfg["webdav_base_url"], cfg["webdav_username"], cfg["webdav_app_password"])
    print(f"Uploading index pages ({len(posts)} posts)...")
    upload_index(dav, posts, cfg)
    print("✓ Index rebuilt.")


def cmd_list():
    posts = load_registry()
    if not posts:
        print("No posts published yet.")
        return
    print(f"\n{'Date':<12}  {'Slug':<35}  Title")
    print("─" * 75)
    for p in posts:
        print(f"{p['date']:<12}  {p['slug']:<35}  {p['title']}")
    print()


def cmd_delete(slug: str, cfg: dict):
    dav = WebDAVClient(cfg["webdav_base_url"], cfg["webdav_username"], cfg["webdav_app_password"])
    blog_path = cfg["blog_path"].strip("/")
    print(f"Deleting {slug}...")
    dav.delete(f"{blog_path}/{slug}/index.html")
    dav.delete(f"{blog_path}/{slug}/")

    posts = load_registry()
    posts = remove_post(posts, slug)
    save_registry(posts)

    print("Uploading index pages...")
    upload_index(dav, posts, cfg)
    print(f"✓ Deleted {slug}.")


# ─────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Fastmail static blog publisher")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("source", nargs="?", type=Path, help="Markdown file to publish")
    group.add_argument("--rebuild-index", action="store_true", help="Regenerate all index pages")
    group.add_argument("--list", action="store_true", help="List published posts")
    group.add_argument("--delete", metavar="SLUG", help="Delete a post by slug")
    group.add_argument("--fix-dates", action="store_true", help="Re-read dates from markdown files and update registry")
    parser.add_argument("--no-index", action="store_true", help="Skip index rebuild (use in batch)")

    args = parser.parse_args()
    cfg = load_config()

    if args.list:
        cmd_list()
    elif args.rebuild_index:
        cmd_rebuild_index(cfg)
    elif args.delete:
        cmd_delete(args.delete, cfg)
    elif args.fix_dates:
        cmd_fix_dates()
    elif args.source:
        cmd_publish(args.source, cfg, no_index=args.no_index)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()