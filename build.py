#!/usr/bin/env python3
"""Gerador estático do blog: lê posts em Markdown e escreve o site em dist/.

Uso: python build.py
Dependências: markdown, pyyaml (requirements-build.txt).
"""
import hashlib
import json
import os
import re
import shutil
import sys
import unicodedata
from datetime import date, datetime, timezone
from email.utils import format_datetime
from html import escape
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
POST_DIRS = [ROOT / "posts_antigos", ROOT / "posts_novos"]
SCRAPE_DATE = "2026-05-06"  # data da raspagem dos posts antigos

DEFAULT_SITE = {
    "name": "Meia vida",
    "description": "Blog pessoal.",
    "author": "Paulo Duarte",
    "url": "https://paulogpd.com.br",
    "lang": "pt-BR",
}

MONTHS = {
    "jan": 1, "feb": 2, "fev": 2, "mar": 3, "apr": 4, "abr": 4, "may": 5,
    "mai": 5, "jun": 6, "jul": 7, "aug": 8, "ago": 8, "sep": 9, "set": 9,
    "oct": 10, "out": 10, "nov": 11, "dec": 12, "dez": 12,
}
BODY_DATE_RE = re.compile(
    r"^[ \t]*_\s*((?:\d{1,2}\s+[A-Za-z]+|[A-Za-z]+\s+\d{1,2}),?\s+\d{4})\s*_[ \t]*$\n?",
    re.M,
)

CSS = """\
:root{--bg:#fafafa;--fg:#1a1a1a;--mut:#666;--line:#ddd;--link:#444;--code:#eee}
@media(prefers-color-scheme:dark){:root{--bg:#161616;--fg:#e4e4e4;--mut:#999;--line:#333;--link:#bbb;--code:#232323}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:1.0625rem/1.7 system-ui,-apple-system,"Segoe UI",sans-serif}
.wrap{max-width:42rem;margin:0 auto;padding:0 1.25rem}
header{padding:2rem 0 1rem;border-bottom:1px solid var(--line)}
header a{font-weight:700;font-size:1.25rem;color:var(--fg);text-decoration:none}
header p{margin:.25rem 0 0;color:var(--mut);font-size:.9rem}
main{padding:1.5rem 0 3rem}
footer{padding:1.5rem 0 3rem;border-top:1px solid var(--line);color:var(--mut);font-size:.875rem}
a{color:var(--link);text-underline-offset:.15em}
a:hover{color:var(--fg)}
h1,h2,h3,h4{line-height:1.25;margin:2rem 0 .75rem}
h1{font-size:1.9rem;margin-top:.5rem}
h2{font-size:1.4rem}h3{font-size:1.15rem}
time,.meta{color:var(--mut);font-size:.9rem}
ul,ol{padding-left:1.4rem}
.posts{list-style:none;padding:0}
.posts li{display:flex;gap:1rem;padding:.2rem 0}
.posts time{flex:0 0 5.5rem;font-variant-numeric:tabular-nums}
blockquote{margin:1.25rem 0;padding:0 1rem;border-left:3px solid var(--line);color:var(--mut)}
code,pre{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.875em}
code{background:var(--code);padding:.1em .3em;border-radius:3px}
pre{background:var(--code);padding:1rem;overflow-x:auto;border-radius:4px}
pre code{background:none;padding:0}
table{border-collapse:collapse;display:block;overflow-x:auto;max-width:100%;font-size:.9rem}
th,td{border:1px solid var(--line);padding:.35rem .6rem;text-align:left}
th{background:var(--code)}
img,iframe,video{max-width:100%;height:auto}
hr{border:0;border-top:1px solid var(--line);margin:2rem 0}
.src{margin-top:2rem;padding-top:1rem;border-top:1px solid var(--line);color:var(--mut);font-size:.9rem}
@media(max-width:30rem){body{font-size:1rem}.posts li{flex-direction:column;gap:0}}
"""


# ── Configuração ────────────────────────────────────────────────────────────

def load_site() -> dict:
    site = dict(DEFAULT_SITE)
    path = ROOT / "site.json"
    if path.exists():
        site.update(json.loads(path.read_text(encoding="utf-8")))
    site["url"] = site["url"].rstrip("/")
    return site


# ── Leitura dos posts ───────────────────────────────────────────────────────

def slugify(text: str) -> str:
    text = unicodedata.normalize("NFD", str(text))
    text = "".join(c for c in text if unicodedata.category(c) != "Mn").lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text.strip())
    return re.sub(r"-+", "-", text).strip("-")


def split_frontmatter(raw: str) -> tuple[dict, str]:
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", raw, re.DOTALL)
    if not m:
        return {}, raw
    try:
        return yaml.safe_load(m.group(1)) or {}, raw[m.end():]
    except yaml.YAMLError:
        return parse_loose_frontmatter(m.group(1)), raw[m.end():]


def parse_loose_frontmatter(text: str) -> dict:
    """Fallback linha a linha, para títulos como '[en] Communism' (YAML inválido)."""
    fm = {}
    for line in text.splitlines():
        key, sep, value = line.partition(":")
        if not sep or not key.strip().isidentifier():
            continue
        try:
            fm[key.strip()] = yaml.safe_load(value)
        except yaml.YAMLError:
            fm[key.strip()] = value.strip()
    return fm


def parse_body_date(text: str) -> str | None:
    """Aceita '12 May, 2025' e 'May 12, 2025'."""
    text = text.strip()
    m = re.fullmatch(r"(\d{1,2})\s+([A-Za-z]+),?\s+(\d{4})", text)
    if m:
        day, month, year = m.groups()
    else:
        m = re.fullmatch(r"([A-Za-z]+)\s+(\d{1,2}),?\s+(\d{4})", text)
        if not m:
            return None
        month, day, year = m.groups()
    num = MONTHS.get(month[:3].lower())
    try:
        return date(int(year), num, int(day)).isoformat() if num else None
    except ValueError:
        return None


def extract_body_date(body: str) -> tuple[str | None, str]:
    """Acha a linha '_ 12 May, 2025 _'. Devolve (data ISO, corpo sem essa linha)."""
    for m in BODY_DATE_RE.finditer(body):
        iso = parse_body_date(m.group(1))
        if iso:
            return iso, body[:m.start()] + body[m.end():]
    return None, body


def drop_duplicate_h1(body: str, title: str) -> str:
    m = re.match(r"\s*#\s+(.+?)\s*\n", body)
    if m and m.group(1).strip().lower() == title.strip().lower():
        return body[m.end():]
    return body


def plain_summary(md_text: str, limit: int = 160) -> str:
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", md_text)
    text = re.sub(r"[#>*_`|\-]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit].rsplit(" ", 1)[0] if len(text) > limit else text


def load_post(path: Path, site: dict, problems: list) -> dict:
    fm, body = split_frontmatter(path.read_text(encoding="utf-8"))
    name = path.relative_to(ROOT).as_posix()

    title = str(fm.get("title") or "").strip()
    if not title:
        h1 = re.match(r"\s*#\s+(.+)", body)
        title = h1.group(1).strip() if h1 else path.stem.replace("-", " ").title()
        problems.append(f"{name}: sem título (usei '{title}')")

    body_date, body = extract_body_date(body)
    fm_date = fm.get("date")
    if isinstance(fm_date, (date, datetime)):
        fm_date = fm_date.strftime("%Y-%m-%d")
    iso = body_date or (str(fm_date) if fm_date else None)
    if not iso:
        iso = date.today().isoformat()
        problems.append(f"{name}: sem data (usei hoje, {iso})")
    elif iso == SCRAPE_DATE and not body_date:
        problems.append(f"{name}: data é a da raspagem ({SCRAPE_DATE}) e não há data no corpo")

    body = drop_duplicate_h1(body, title)
    tags = fm.get("tags") or []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",")]
    slug = str(fm.get("slug") or "").strip("/ ") or slugify(title)
    if not slug:
        slug = slugify(path.stem)

    return {
        "path": path,
        "file": name,
        "title": title,
        "date": iso,
        "slug": slug,
        "description": str(fm.get("description") or "").strip() or plain_summary(body),
        "tags": tags,
        "source": fm.get("source"),
        "lang": fm.get("lang") or site["lang"],
        "body": body,
    }


def load_posts(site: dict, problems: list) -> list[dict]:
    posts = []
    for folder in POST_DIRS:
        for path in sorted(folder.glob("*.md")):
            posts.append(load_post(path, site, problems))
    return posts


def check_slugs(posts: list[dict]) -> None:
    seen: dict[str, list[str]] = {}
    for p in posts:
        seen.setdefault(p["slug"], []).append(p["file"])
    dups = {s: f for s, f in seen.items() if len(f) > 1}
    if dups:
        print("ERRO: slugs duplicados. Defina 'slug:' no frontmatter de um dos arquivos:")
        for slug, files in dups.items():
            print(f"  /{slug}/ -> {', '.join(files)}")
        sys.exit(1)


# ── Markdown → HTML ─────────────────────────────────────────────────────────

def render_markdown(body: str) -> str:
    md = markdown.Markdown(extensions=["fenced_code", "tables", "footnotes", "attr_list"])
    return md.convert(body)


def copy_local_images(post: dict, html: str) -> str:
    """Copia imagens locais referenciadas para dist/<slug>/ e ajusta o src."""
    def fix(m: re.Match) -> str:
        src = m.group(2)
        if re.match(r"^(https?:)?//|^data:|^/", src):
            return m.group(0)
        for base in (post["path"].parent, ROOT):
            origin = (base / src).resolve()
            if origin.is_file() and ROOT in origin.parents:
                dest = DIST / post["slug"]
                dest.mkdir(parents=True, exist_ok=True)
                shutil.copy2(origin, dest / origin.name)
                return f'{m.group(1)}{origin.name}{m.group(3)}'
        return m.group(0)

    return re.sub(r'(<img[^>]*\ssrc=")([^"]+)(")', fix, html)


# ── Templates ───────────────────────────────────────────────────────────────

def page(site: dict, css_v: str, *, title: str, desc: str, url: str, lang: str,
         content: str, og_type: str = "website") -> str:
    full_title = f"{title} | {site['name']}" if title != site["name"] else site["name"]
    return f"""<!doctype html>
<html lang="{escape(lang)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(full_title)}</title>
<meta name="description" content="{escape(desc, quote=True)}">
<link rel="canonical" href="{escape(url)}">
<link rel="alternate" type="application/rss+xml" title="{escape(site['name'])}" href="/feed.xml">
<link rel="stylesheet" href="/style.css?v={css_v}">
<meta property="og:title" content="{escape(title, quote=True)}">
<meta property="og:description" content="{escape(desc, quote=True)}">
<meta property="og:url" content="{escape(url)}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{escape(site['name'], quote=True)}">
</head>
<body>
<div class="wrap">
<header><a href="/">{escape(site['name'])}</a><p>{escape(site['description'])}</p></header>
<main>
{content}
</main>
<footer>&copy; {datetime.now().year} {escape(site['author'])} &middot; <a href="/feed.xml">RSS</a></footer>
</div>
</body>
</html>
"""


def render_post(site: dict, css_v: str, post: dict, html_body: str) -> str:
    src = ""
    if post["source"]:
        link = escape(str(post["source"]), quote=True)
        src = f'\n<p class="src">Publicado originalmente em <a href="{link}">{link}</a></p>'
    content = (
        f'<article>\n<h1>{escape(post["title"])}</h1>\n'
        f'<p class="meta"><time datetime="{post["date"]}">{post["date"]}</time></p>\n'
        f'{html_body}{src}\n</article>'
    )
    return page(site, css_v, title=post["title"], desc=post["description"],
                url=f'{site["url"]}/{post["slug"]}/', lang=post["lang"],
                content=content, og_type="article")


def render_index(site: dict, css_v: str, posts: list[dict]) -> str:
    parts, year = [], None
    for p in posts:
        y = p["date"][:4]
        if y != year:
            if year:
                parts.append("</ul>")
            parts.append(f"<h2>{y}</h2>\n<ul class=\"posts\">")
            year = y
        parts.append(
            f'<li><time datetime="{p["date"]}">{p["date"][5:]}</time>'
            f'<a href="/{p["slug"]}/">{escape(p["title"])}</a></li>'
        )
    if year:
        parts.append("</ul>")
    return page(site, css_v, title=site["name"], desc=site["description"],
                url=site["url"] + "/", lang=site["lang"], content="\n".join(parts))


def render_404(site: dict, css_v: str) -> str:
    content = '<h1>Página não encontrada</h1>\n<p><a href="/">Voltar para a home</a></p>'
    return page(site, css_v, title="Página não encontrada", desc="Página não encontrada.",
                url=site["url"] + "/404.html", lang=site["lang"], content=content)


def render_rss(site: dict, posts: list[dict]) -> str:
    base = site["url"]
    items = []
    for p in posts[:20]:
        pub = format_datetime(datetime.strptime(p["date"], "%Y-%m-%d").replace(tzinfo=timezone.utc))
        link = f'{base}/{p["slug"]}/'
        items.append(
            "  <item>\n"
            f"    <title>{escape(p['title'])}</title>\n"
            f"    <link>{escape(link)}</link>\n"
            f'    <guid isPermaLink="true">{escape(link)}</guid>\n'
            f"    <pubDate>{pub}</pubDate>\n"
            f"    <description>{escape(p['description'])}</description>\n"
            "  </item>"
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n<channel>\n'
        f"  <title>{escape(site['name'])}</title>\n"
        f"  <link>{base}/</link>\n"
        f"  <description>{escape(site['description'])}</description>\n"
        f"  <language>{escape(site['lang'])}</language>\n"
        f'  <atom:link href="{base}/feed.xml" rel="self" type="application/rss+xml"/>\n'
        + "\n".join(items) + "\n</channel>\n</rss>\n"
    )


def render_sitemap(site: dict, posts: list[dict]) -> str:
    urls = [f"  <url><loc>{site['url']}/</loc></url>"]
    urls += [
        f"  <url><loc>{escape(site['url'])}/{escape(p['slug'])}/</loc><lastmod>{p['date']}</lastmod></url>"
        for p in posts
    ]
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(urls) + "\n</urlset>\n")


# ── Build ───────────────────────────────────────────────────────────────────

def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    site = load_site()
    # No Netlify, a variável URL tem o endereço público do deploy (útil antes do domínio próprio).
    if os.environ.get("NETLIFY") and not (ROOT / "site.json").exists() and os.environ.get("URL"):
        site["url"] = os.environ["URL"].rstrip("/")

    problems: list[str] = []
    posts = load_posts(site, problems)
    check_slugs(posts)
    posts.sort(key=lambda p: (p["date"], p["title"]), reverse=True)

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()

    css_v = hashlib.md5(CSS.encode()).hexdigest()[:8]
    write(DIST / "style.css", CSS)
    for p in posts:
        html = copy_local_images(p, render_markdown(p["body"]))
        write(DIST / p["slug"] / "index.html", render_post(site, css_v, p, html))
    write(DIST / "index.html", render_index(site, css_v, posts))
    write(DIST / "404.html", render_404(site, css_v))
    write(DIST / "feed.xml", render_rss(site, posts))
    write(DIST / "sitemap.xml", render_sitemap(site, posts))
    write(DIST / "robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {site['url']}/sitemap.xml\n")

    print(f"{len(posts)} posts gerados em {DIST.relative_to(ROOT)}/")
    for line in problems:
        print(f"  aviso: {line}")


if __name__ == "__main__":
    main()
