# fastmail-blog

> \[!NOTE]
> 
> For the PTBR version, access the [README.pt.md](https://github.com/mtgr18977/blog/blob/master/README.pt.md).
> 
> For the webv version (using `flask`) access the [README_WEB.md](https://github.com/mtgr18977/blog/blob/master/README_WEB.md) version.

A minimal static blog system that publishes Markdown posts directly to **Fastmail Files** via WebDAV. No build step, no server, no framework — just Python and your writing.

---

## How it works

```
Markdown file (.md)
      ↓
  publish.py
      ↓
 HTML page (with inline CSS)
      ↓
 Fastmail WebDAV (your domain)
```

Posts are converted from Markdown to self-contained HTML pages and uploaded to your Fastmail Files storage, which can be served as a static website through your custom domain.

---

## Requirements

- Python 3.10+
- A [Fastmail](https://fastmail.com) account with Files & Storage enabled
- A custom domain pointed to Fastmail (optional but recommended)

Install dependencies:

```bash
pip install requests markdown pyyaml
```

Or with `uv`:

```bash
uv pip install requests markdown pyyaml
```

---

## Setup

**1. Copy the config template:**

```bash
cp .blog-config.example.json .blog-config.json
```

**2. Fill in your credentials:**

```json
{
  "webdav_base_url": "https://myfiles.fastmail.com/",
  "webdav_username": "you@fastmail.com",
  "webdav_app_password": "YOUR_APP_PASSWORD",
  "blog_path": "blog/",
  "site_title": "My Blog",
  "site_description": "A short description",
  "author": "Your Name",
  "base_url": "https://yourdomain.com/blog/",
  "posts_per_page": 10
}
```

To generate a Fastmail app password: **Settings → Privacy & Security → Manage app passwords**

To find your WebDAV URL: **Settings → Files & Storage**

> `.blog-config.json` is in `.gitignore` — never commit your credentials.

---

## Writing posts

Posts are plain Markdown files with YAML frontmatter:

```markdown
---
title: My first post
date: 2024-01-15
description: A short summary shown in the index.
tags: [writing, personal]
---

Your content here.
```

| Field         | Required | Description                            |
|---------------|----------|----------------------------------------|
| `title`       | No       | Defaults to the filename               |
| `date`        | No       | Defaults to today                      |
| `description` | No       | Shown in the post index                |
| `tags`        | No       | List or comma-separated string         |
| `slug`        | No       | URL slug; auto-generated from title    |

Supported Markdown extensions: fenced code blocks, tables, footnotes, table of contents, syntax highlighting.

---

## Publishing

```bash
# Publish a single post
python publish.py my-post.md

# Rebuild the entire index (after editing multiple posts)
python publish.py --rebuild-index

# List all published posts
python publish.py --list

# Delete a post by its slug
python publish.py --delete my-post-slug
```

---

## Importing existing posts

`scrap_blog.py` scrapes an existing blog and saves each post as a Markdown file compatible with `publish.py`:

```bash
# Save to current directory
python scrap_blog.py

# Save to a specific folder
python scrap_blog.py posts_antigos/
```

Edit `BLOG_INDEX_URL` inside the script to point to your source blog.

---

## Directory structure

```
.
├── publish.py               # Main publisher
├── scrap_blog.py            # Blog scraper / importer
├── .blog-config.json        # Your credentials (gitignored)
├── .blog-config.example.json
├── .blog-posts.json         # Local post registry (auto-managed)
├── preview-index.html       # Local preview of the index page
├── preview-post.html        # Local preview of a post page
├── posts_antigos/           # Imported/archived posts
└── posts_novos/             # New posts to publish
```

---

## Design

The generated HTML is self-contained with inline CSS. The default theme uses:

- **Fonts**: Josefin Sans (headings), Lora (body), JetBrains Mono (code)
- **Colors**: Dark background (`#1a2332`) with teal accents
- **Layout**: Single-column, max 720px, responsive

To customize the design, edit the `CSS` constant in `publish.py`.

---

## License

MIT
