#!/usr/bin/env python3
"""
Fastmail Blog Publisher - Web Interface
Flask app that allows publishing markdown posts to Fastmail via WebDAV
"""

import os
import sys
import json
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, request, render_template_string, redirect, url_for, flash, session
from flask_wtf.csrf import CSRFProtect
import bleach

# Import functions from publish.py
sys.path.insert(0, str(Path(__file__).parent))
from publish import (
    parse_markdown, resolve_meta, extract_date_from_body, slugify,
    render_post, load_registry, upsert_post, save_registry,
    WebDAVClient, CSS, DEFAULT_CONFIG, CONFIG_FILE
)

app = Flask(__name__)

# SECRET_KEY must be set via environment variable - never hardcode secrets!
if not os.environ.get("SECRET_KEY"):
    raise RuntimeError(
        "SECRET_KEY environment variable is required. "
        "Generate one with: python -c 'import secrets; print(secrets.token_hex(32))' "
        "Then export it: export SECRET_KEY='<your-key>'"
    )
app.secret_key = os.environ["SECRET_KEY"]

# Enable CSRF protection for all forms
csrf = CSRFProtect(app)

# ─────────────────────────────────────────
# HTML Templates
# ─────────────────────────────────────────

BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Blog Publisher{% endblock %}</title>
    <style>
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
            --success:      #4caf50;
            --error:        #f44336;
            --warning:      #ff9800;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            background: var(--bg);
            color: var(--text);
            font-family: var(--font-body, 'Lora', Georgia, serif);
            line-height: 1.6;
            min-height: 100vh;
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem;
        }

        header {
            padding: 2rem 0;
            border-bottom: 1px solid var(--border);
            margin-bottom: 2rem;
        }

        h1 {
            font-family: 'Josefin Sans', system-ui, sans-serif;
            font-weight: 700;
            font-size: 1.8rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--accent-hover);
        }

        .nav-links {
            margin-top: 1rem;
            display: flex;
            gap: 1rem;
        }

        .nav-links a {
            font-family: 'Josefin Sans', system-ui, sans-serif;
            font-size: 0.75rem;
            color: var(--muted);
            text-decoration: none;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            padding: 0.4em 0.9em;
            border: 1px solid var(--border);
            border-radius: 3px;
            transition: color 0.2s, border-color 0.2s;
        }

        .nav-links a:hover {
            color: var(--accent-hover);
            border-color: var(--accent);
        }

        .flash-messages {
            margin-bottom: 1.5rem;
        }

        .flash {
            padding: 1rem;
            border-radius: 3px;
            margin-bottom: 0.5rem;
            font-family: 'Josefin Sans', system-ui, sans-serif;
            font-size: 0.85rem;
        }

        .flash.success { background: rgba(76, 175, 80, 0.2); border: 1px solid var(--success); }
        .flash.error { background: rgba(244, 67, 54, 0.2); border: 1px solid var(--error); }
        .flash.warning { background: rgba(255, 152, 0, 0.2); border: 1px solid var(--warning); }

        form {
            background: var(--surface);
            padding: 2rem;
            border-radius: 3px;
            border: 1px solid var(--border);
        }

        .form-group {
            margin-bottom: 1.5rem;
        }

        label {
            display: block;
            font-family: 'Josefin Sans', system-ui, sans-serif;
            font-size: 0.75rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--accent);
            margin-bottom: 0.5rem;
        }

        input[type="text"],
        input[type="password"],
        textarea {
            width: 100%;
            background: var(--bg);
            border: 1px solid var(--border);
            border-radius: 3px;
            color: var(--text);
            font-family: 'Lora', Georgia, serif;
            font-size: 1rem;
            padding: 0.75rem;
            outline: none;
            transition: border-color 0.2s;
        }

        input:focus,
        textarea:focus {
            border-color: var(--accent);
        }

        textarea {
            min-height: 400px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
            line-height: 1.5;
            resize: vertical;
        }

        .help-text {
            font-family: 'Josefin Sans', system-ui, sans-serif;
            font-size: 0.75rem;
            color: var(--muted);
            margin-top: 0.5rem;
        }

        button {
            background: var(--accent);
            color: var(--bg);
            font-family: 'Josefin Sans', system-ui, sans-serif;
            font-size: 0.85rem;
            font-weight: 600;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            padding: 0.75rem 2rem;
            border: none;
            border-radius: 3px;
            cursor: pointer;
            transition: background 0.2s;
        }

        button:hover {
            background: var(--accent-hover);
        }

        button.secondary {
            background: transparent;
            color: var(--muted);
            border: 1px solid var(--border);
        }

        button.secondary:hover {
            color: var(--accent-hover);
            border-color: var(--accent);
        }

        .config-section {
            margin-bottom: 2rem;
            padding: 1.5rem;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 3px;
        }

        .config-status {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }

        .status-indicator {
            width: 10px;
            height: 10px;
            border-radius: 50%;
        }

        .status-indicator.ok { background: var(--success); }
        .status-indicator.missing { background: var(--warning); }

        .btn-group {
            display: flex;
            gap: 1rem;
            margin-top: 1.5rem;
        }

        .preview-section {
            margin-top: 2rem;
            padding: 2rem;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 3px;
        }

        .preview-content {
            background: var(--bg);
            padding: 1.5rem;
            border-radius: 3px;
            margin-top: 1rem;
            max-height: 500px;
            overflow-y: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-family: 'Josefin Sans', system-ui, sans-serif;
            font-size: 0.85rem;
            margin: 1rem 0;
        }

        th, td {
            border: 1px solid var(--border);
            padding: 0.5rem;
            text-align: left;
        }

        th {
            background: var(--bg);
            color: var(--accent);
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.7rem;
            letter-spacing: 0.08em;
        }

        tr:nth-child(even) td { background: var(--bg); }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📝 Blog Publisher</h1>
            <div class="nav-links">
                <a href="{{ url_for('index') }}">Publicar</a>
                <a href="{{ url_for('config_page') }}">Configuração</a>
                <a href="{{ url_for('list_posts') }}">Posts Publicados</a>
            </div>
        </header>

        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                <div class="flash-messages">
                    {% for category, message in messages %}
                        <div class="flash {{ category }}">{{ message }}</div>
                    {% endfor %}
                </div>
            {% endif %}
        {% endwith %}

        {% block content %}{% endblock %}
    </div>
</body>
</html>
"""

INDEX_TEMPLATE = """
{% extends "base" %}
{% block title %}Publicar Post - Blog Publisher{% endblock %}
{% block content %}
<form method="POST" action="{{ url_for('publish') }}">
    <div class="form-group">
        <label for="markdown">Conteúdo Markdown</label>
        <textarea id="markdown" name="markdown" placeholder="Cole seu arquivo markdown aqui...

---
title: Meu Post
date: 2024-01-15
description: Uma breve descrição
tags: python, blog
---

Conteúdo do post..."></textarea>
        <div class="help-text">
            Inclua o frontmatter YAML entre --- no início do arquivo.
            O sistema extrairá título, data, descrição e tags automaticamente.
        </div>
    </div>
    
    <div class="btn-group">
        <button type="submit">🚀 Publicar no Fastmail</button>
        <button type="button" class="secondary" onclick="previewPost()">👁️ Preview</button>
    </div>
</form>

<div id="preview" class="preview-section" style="display: none;">
    <h2 style="font-family: 'Josefin Sans'; font-size: 1.2rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--accent);">Preview</h2>
    <div id="preview-content" class="preview-content"></div>
</div>

<script>
function previewPost() {
    const markdown = document.getElementById('markdown').value;
    const previewDiv = document.getElementById('preview');
    const contentDiv = document.getElementById('preview-content');
    
    fetch('/api/preview', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({markdown: markdown})
    })
    .then(r => r.json())
    .then(data => {
        if (data.html) {
            contentDiv.innerHTML = data.html;
            previewDiv.style.display = 'block';
            previewDiv.scrollIntoView({behavior: 'smooth'});
        }
    });
}
</script>
{% endblock %}
"""

CONFIG_TEMPLATE = """
{% extends "base" %}
{% block title %}Configuração - Blog Publisher{% endblock %}
{% block content %}
<div class="config-section">
    <div class="config-status">
        <div class="status-indicator {{ 'ok' if config_exists else 'missing' }}"></div>
        <span>{{ 'Configuração encontrada' if config_exists else 'Nenhuma configuração salva' }}</span>
    </div>
    
    {% if config_exists %}
        <table>
            <tr><th>Parâmetro</th><th>Valor</th></tr>
            <tr><td>WebDAV URL</td><td>{{ config.webdav_base_url }}</td></tr>
            <tr><td>Username</td><td>{{ config.webdav_username }}</td></tr>
            <tr><td>Blog Path</td><td>{{ config.blog_path }}</td></tr>
            <tr><td>Site Title</td><td>{{ config.site_title }}</td></tr>
            <tr><td>Base URL</td><td>{{ config.base_url }}</td></tr>
        </table>
    {% endif %}
</div>

<form method="POST" action="{{ url_for('save_config') }}">
    <div class="form-group">
        <label for="webdav_base_url">WebDAV Base URL</label>
        <input type="text" id="webdav_base_url" name="webdav_base_url" 
               value="{{ config.webdav_base_url if config else 'https://myfiles.fastmail.com/' }}" required>
        <div class="help-text">URL do WebDAV do Fastmail (geralmente https://myfiles.fastmail.com/)</div>
    </div>
    
    <div class="form-group">
        <label for="webdav_username">WebDAV Username</label>
        <input type="text" id="webdav_username" name="webdav_username" 
               value="{{ config.webdav_username if config else '' }}" required>
        <div class="help-text">Seu email do Fastmail ou username do WebDAV</div>
    </div>
    
    <div class="form-group">
        <label for="webdav_app_password">WebDAV App Password</label>
        <input type="password" id="webdav_app_password" name="webdav_app_password"
               value="" autocomplete="off" required>
        <div class="help-text">Senha de aplicativo gerada em Fastmail → Settings → Privacy & Security</div>
        {% if config and config.webdav_app_password %}
        <div class="help-text" style="color: var(--muted); font-size: 0.85rem; margin-top: 0.3rem;">
            ✓ Senha já configurada (não exibida por segurança)
        </div>
        {% endif %}
    </div>
    
    <div class="form-group">
        <label for="blog_path">Blog Path</label>
        <input type="text" id="blog_path" name="blog_path" 
               value="{{ config.blog_path if config else 'blog/' }}">
        <div class="help-text">Caminho da pasta no Fastmail Files (ex: blog/)</div>
    </div>
    
    <div class="form-group">
        <label for="site_title">Título do Site</label>
        <input type="text" id="site_title" name="site_title" 
               value="{{ config.site_title if config else 'My Blog' }}">
    </div>
    
    <div class="form-group">
        <label for="site_description">Descrição do Site</label>
        <input type="text" id="site_description" name="site_description" 
               value="{{ config.site_description if config else '' }}">
    </div>
    
    <div class="form-group">
        <label for="author">Autor</label>
        <input type="text" id="author" name="author" 
               value="{{ config.author if config else '' }}">
    </div>
    
    <div class="form-group">
        <label for="base_url">Base URL do Blog</label>
        <input type="text" id="base_url" name="base_url" 
               value="{{ config.base_url if config else 'https://yourdomain.com/blog/' }}">
        <div class="help-text">URL pública onde seu blog estará disponível</div>
    </div>
    
    <div class="form-group">
        <label for="posts_per_page">Posts por Página</label>
        <input type="text" id="posts_per_page" name="posts_per_page" 
               value="{{ config.posts_per_page if config else 10 }}">
    </div>
    
    <button type="submit">💾 Salvar Configuração</button>
</form>
{% endblock %}
"""

LIST_TEMPLATE = """
{% extends "base" %}
{% block title %}Posts Publicados - Blog Publisher{% endblock %}
{% block content %}
<h2 style="font-family: 'Josefin Sans'; font-size: 1.4rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--accent); margin-bottom: 1.5rem;">
    Posts Publicados
</h2>

{% if posts %}
<table>
    <thead>
        <tr>
            <th>Data</th>
            <th>Slug</th>
            <th>Título</th>
            <th>Ações</th>
        </tr>
    </thead>
    <tbody>
        {% for post in posts %}
        <tr>
            <td>{{ post.date }}</td>
            <td>{{ post.slug }}</td>
            <td>{{ post.title }}</td>
            <td>
                <form method="POST" action="{{ url_for('delete_post') }}" style="display: inline;" onsubmit="return confirm('Tem certeza que deseja deletar este post?');">
                    <input type="hidden" name="slug" value="{{ post.slug }}">
                    <button type="submit" class="secondary" style="padding: 0.4em 0.8em; font-size: 0.7rem;">🗑️ Deletar</button>
                </form>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% else %}
<p style="color: var(--muted); font-family: 'Josefin Sans'; font-size: 0.9rem;">Nenhum post publicado ainda.</p>
{% endif %}

<div style="margin-top: 2rem;">
    <a href="{{ url_for('rebuild_index') }}">
        <button class="secondary">🔄 Rebuild Index</button>
    </a>
</div>
{% endblock %}
"""

app.jinja_env.from_string(BASE_TEMPLATE)


def load_config() -> dict:
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            cfg = json.load(f)
        for k, v in DEFAULT_CONFIG.items():
            cfg.setdefault(k, v)
        return cfg
    return DEFAULT_CONFIG.copy()


def save_config_file(cfg: dict):
    import stat
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)
    # Set file permissions to 600 (owner read/write only) for security
    os.chmod(CONFIG_FILE, stat.S_IRUSR | stat.S_IWUSR)


@app.route("/")
def index():
    return render_template_string(INDEX_TEMPLATE.replace('{% extends "base" %}', BASE_TEMPLATE))


@app.route("/config")
def config_page():
    cfg = load_config()
    config_exists = CONFIG_FILE.exists()
    return render_template_string(
        CONFIG_TEMPLATE.replace('{% extends "base" %}', BASE_TEMPLATE),
        config=cfg if config_exists else None,
        config_exists=config_exists
    )


@app.route("/config/save", methods=["POST"])
def save_config():
    cfg = {
        "webdav_base_url": request.form.get("webdav_base_url", DEFAULT_CONFIG["webdav_base_url"]),
        "webdav_username": request.form.get("webdav_username", ""),
        "webdav_app_password": request.form.get("webdav_app_password", ""),
        "blog_path": request.form.get("blog_path", DEFAULT_CONFIG["blog_path"]),
        "site_title": request.form.get("site_title", DEFAULT_CONFIG["site_title"]),
        "site_description": request.form.get("site_description", DEFAULT_CONFIG["site_description"]),
        "author": request.form.get("author", DEFAULT_CONFIG["author"]),
        "base_url": request.form.get("base_url", DEFAULT_CONFIG["base_url"]),
        "posts_per_page": int(request.form.get("posts_per_page", DEFAULT_CONFIG["posts_per_page"])),
    }
    save_config_file(cfg)
    flash("Configuração salva com sucesso!", "success")
    return redirect(url_for("config_page"))


@app.route("/publish", methods=["POST"])
def publish():
    markdown_content = request.form.get("markdown", "")
    
    if not markdown_content.strip():
        flash("Por favor, cole o conteúdo markdown.", "error")
        return redirect(url_for("index"))
    
    cfg = load_config()
    
    # Check if config is complete
    if not cfg.get("webdav_username") or not cfg.get("webdav_app_password"):
        flash("Configuração incompleta. Por favor, configure suas credenciais do WebDAV primeiro.", "warning")
        return redirect(url_for("config_page"))
    
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write(markdown_content)
            temp_path = Path(f.name)
        
        try:
            # Parse markdown
            frontmatter, html_body = parse_markdown(temp_path)
            meta = resolve_meta(frontmatter, temp_path)
            
            _body_date = extract_date_from_body(markdown_content)
            date_source = "(from body)" if _body_date else "(from frontmatter)" if frontmatter.get("date") else "(today)"
            
            # Render HTML
            post_html = render_post(meta, html_body, cfg)
            
            # Connect to WebDAV
            dav = WebDAVClient(cfg["webdav_base_url"], cfg["webdav_username"], cfg["webdav_app_password"])
            
            if not dav.test_connection():
                flash("Não foi possível conectar ao Fastmail. Verifique suas credenciais.", "error")
                return redirect(url_for("index"))
            
            blog_path = cfg["blog_path"].strip("/")
            slug = meta["slug"]
            
            # Upload post
            dav.mkcol(blog_path)
            dav.mkcol(f"{blog_path}/{slug}")
            
            ok = dav.put(f"{blog_path}/{slug}/index.html", post_html)
            if not ok:
                flash("Falha ao upload do post.", "error")
                return redirect(url_for("index"))
            
            # Update registry
            posts = load_registry()
            posts = upsert_post(posts, meta)
            save_registry(posts)
            
            # Upload index
            from publish import upload_index
            upload_index(dav, posts, cfg)
            
            flash(f"✓ Post publicado com sucesso! → {cfg['base_url']}{slug}/", "success")
            
        finally:
            # Cleanup temp file
            temp_path.unlink(missing_ok=True)
            
    except Exception as e:
        flash(f"Erro ao publicar: {str(e)}", "error")
        import traceback
        traceback.print_exc()
    
    return redirect(url_for("index"))

@app.route("/api/preview", methods=["POST"])
def preview():
    data = request.get_json()
    if not data:
        return {"html": "<p>Dados inválidos.</p>"}
    
    markdown_content = data.get("markdown", "")

    if not markdown_content.strip():
        return {"html": "<p>Nenhum conteúdo fornecido.</p>"}

    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write(markdown_content)
            temp_path = Path(f.name)

        try:
            _, html_body = parse_markdown(temp_path)
            # Sanitize HTML to prevent XSS
            clean_html = bleach.clean(
                html_body,
                tags=[
                    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                    'p', 'br', 'hr',
                    'strong', 'em', 'b', 'i', 'u', 's', 'strike',
                    'a', 'ul', 'ol', 'li',
                    'blockquote', 'pre', 'code',
                    'table', 'thead', 'tbody', 'tr', 'th', 'td',
                    'img', 'figure', 'figcaption'
                ],
                attributes={
                    'a': ['href', 'title', 'target', 'rel'],
                    'img': ['src', 'alt', 'title'],
                    'code': ['class'],
                    'pre': ['class']
                },
                protocols=['http', 'https'],
                strip=True
            )
            return {"html": clean_html}
        finally:
            temp_path.unlink(missing_ok=True)
    except Exception as e:
        return {"html": f"<p style='color: red;'>Erro: {str(e)}</p>"}


@app.route("/posts")
def list_posts():
    posts = load_registry()
    return render_template_string(
        LIST_TEMPLATE.replace('{% extends "base" %}', BASE_TEMPLATE),
        posts=posts
    )


@app.route("/posts/delete", methods=["POST"])
def delete_post():
    slug = request.form.get("slug", "")
    
    if not slug:
        flash("Slug inválido.", "error")
        return redirect(url_for("list_posts"))
    
    cfg = load_config()
    
    try:
        dav = WebDAVClient(cfg["webdav_base_url"], cfg["webdav_username"], cfg["webdav_app_password"])
        blog_path = cfg["blog_path"].strip("/")
        
        dav.delete(f"{blog_path}/{slug}/index.html")
        dav.delete(f"{blog_path}/{slug}/")
        
        posts = load_registry()
        from publish import remove_post
        posts = remove_post(posts, slug)
        save_registry(posts)
        
        # Rebuild index
        from publish import upload_index
        upload_index(dav, posts, cfg)
        
        flash(f"Post '{slug}' deletado com sucesso.", "success")
    except Exception as e:
        flash(f"Erro ao deletar: {str(e)}", "error")
    
    return redirect(url_for("list_posts"))


@app.route("/posts/rebuild-index")
def rebuild_index():
    cfg = load_config()
    posts = load_registry()
    
    if not posts:
        flash("Nenhum post no registry.", "warning")
        return redirect(url_for("list_posts"))
    
    try:
        dav = WebDAVClient(cfg["webdav_base_url"], cfg["webdav_username"], cfg["webdav_app_password"])
        from publish import upload_index
        upload_index(dav, posts, cfg)
        flash("Index rebuilt com sucesso.", "success")
    except Exception as e:
        flash(f"Erro ao rebuild: {str(e)}", "error")
    
    return redirect(url_for("list_posts"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # SECURITY: Debug mode defaults to False for production safety
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    if debug:
        print("WARNING: Debug mode is ENABLED. Do not use in production!")
    print(f"Starting Blog Publisher Web Interface on http://localhost:{port}")
    print("Configure your Fastmail credentials at /config first.")
    # SECURITY: Only bind to localhost unless explicitly configured
    host = os.environ.get("FLASK_HOST", "127.0.0.1")
    app.run(host=host, port=port, debug=debug)
