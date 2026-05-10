---
title: I Built a Blog With a WebDAV API and Some Python
date: 2026-05-10
slug: i-built-a-blog-with-webdav-and-python
description: How I turned my Fastmail file storage into a static blog publisher with 300 lines of Python and no deployment pipeline.
tags: [python, web, fastmail, tools]
---

I already pay for Fastmail. I pay for the email, the calendar, the contacts sync, the custom domain. And somewhere in that subscription, quietly sitting there, is file storage — accessible via WebDAV, serveable over HTTP, pointed at my own domain.

That's a web host. I was already paying for a web host and didn't know it.

So I built a blog on it.

## The problem with most static site setups

I've tried the usual suspects. Hugo, Jekyll, Eleventy. They're fine — genuinely good pieces of software — but they come with a cost that isn't measured in money: they come with a *pipeline*. You write Markdown, you run a build command, you push to a repository, something deploys. There are configuration files. There are themes with their own configuration files. There are dependencies that break when you update Node.

I don't want a pipeline. I want to write something and have it appear on the internet.

## What Fastmail actually gives you

Fastmail supports several open protocols for accessing your data. Mail goes through JMAP or IMAP. Contacts sync via CardDAV. Files — the ones relevant here — are accessible via WebDAV.

WebDAV is old. It's an extension of HTTP from 1996 that adds methods like `MKCOL` (make collection, i.e. create a directory) and `PROPFIND` (list directory contents). Every Fastmail account gets a WebDAV endpoint, and files stored there can be served directly over HTTP if you configure your domain to point at them.

That's the entire infrastructure.

## The publish.py script

The core of the system is a single Python file — `publish.py` — that does three things:

1. Parses a Markdown file with YAML frontmatter
2. Renders it into a self-contained HTML file with embedded CSS
3. Uploads it to Fastmail via WebDAV

```python
python publish.py my-post.md
```

That's the entire deploy command. No build step. No git push. No CI/CD. One command, one file on the internet.

The frontmatter is minimal:

```yaml
---
title: My Post Title
date: 2026-05-10
slug: my-post-title
description: One sentence about the post.
tags: [python, tools]
---
```

All fields are optional. If you omit the title, it derives one from the filename. If you omit the date, it uses today. If you omit the slug, it slugifies the title. You can write a post with no frontmatter at all and it will still publish correctly.

## Structure on the server

Every post lives in its own directory, so URLs are clean:

```
blog/
├── index.html              ← paginated post listing
├── page/2/index.html       ← older posts
├── search/index.html       ← search page
├── search.json             ← search index (fetched by JS)
├── my-post/
│   └── index.html
└── another-post/
    └── index.html
```

The index is rebuilt automatically on every publish. Pagination is static — no JavaScript required for navigation, just pre-generated HTML pages. The search, however, does use JavaScript: a small fetch call that loads `search.json` and filters in real time as you type. No external search library, no backend, no Algolia.

## The scraper

This blog has a history. I wrote things before — scattered across a previous setup — and I wanted to bring them over without doing it by hand.

So before the publisher, I wrote a scraper:

```python
python scraper.py posts/
```

It hits the old blog's index page, finds all the post links, fetches each one, extracts the content, converts the HTML to Markdown with `html2text`, and saves each file with a slug derived from the URL — not the title, because the title extraction was unreliable and I kept getting fifteen files called the same thing.

Then a small `fix_titles.py` script corrected the frontmatter by reading the first `# Heading` in the body of each file and using that as the canonical title.

Three scripts, maybe 400 lines total. Migration done.

## What I learned

**WebDAV is underrated.** It's not sexy, it's not in any tutorial, but it works everywhere, it requires no special server software, and authentication is just HTTP Basic — a username and an app password. The Fastmail WebDAV endpoint responded correctly to every request on the first try.

**Static is the right default.** Every dynamic feature I've added to websites over the years has been a maintenance liability. Databases need backups. Servers need updates. Dependencies accumulate. A folder of HTML files does not have these problems. A folder of HTML files will still work in thirty years.

**Owning your infrastructure matters.** I'm not on someone else's publishing platform. My posts aren't subject to a terms of service change, a pricing restructure, or a sunset announcement. The files live in my Fastmail account, which I control, pointed at my domain, which I own.

The search index is a JSON file. The posts are HTML. The styles are embedded in each file. If Fastmail disappeared tomorrow, I could take the files, put them anywhere that serves HTTP, and nothing would break.

## What's missing

There's no image hosting — images need to be uploaded separately through the Fastmail web interface or another WebDAV call. There's no RSS feed, though that would be a small addition: generate `feed.xml` alongside `index.html` during the index rebuild.

There's no comments section, and I'm not sure I want one.

There's no analytics, and I'm certain I don't want those.

## The point

I wrote this system in an afternoon, debugging the WebDAV URL mostly. The result is a blog that costs nothing extra to run, deploys with a single command, has no build pipeline, no dependencies beyond three Python packages, and lives on infrastructure I already own.

That feels right.
