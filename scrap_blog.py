"""
Scraper para https://herebedragons.com.br/blog/
Salva cada post como Markdown compatível com publish.py.

Uso:
    python scraper.py                          # salva no diretório atual
    python scraper.py posts_completos/         # salva em pasta específica
    python scraper.py /caminho/absoluto/       # salva em caminho absoluto
"""

import requests
from bs4 import BeautifulSoup
import html2text
import os
import sys
from datetime import datetime
from urllib.parse import urljoin

# ===== CONFIGURAÇÃO =====
BLOG_INDEX_URL = "https://herebedragons.com.br/blog/"
PASTA_SAIDA = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
# =========================

os.makedirs(PASTA_SAIDA, exist_ok=True)
print(f"📁 Salvando em: {os.path.abspath(PASTA_SAIDA)}")

conversor_md = html2text.HTML2Text()
conversor_md.ignore_links = False
conversor_md.ignore_images = False
conversor_md.body_width = 0


def slug_da_url(url):
    """Extrai o slug final da URL do post."""
    partes = url.rstrip("/").split("/")
    return partes[-1] or partes[-2]


def obter_links():
    print("🔍 Buscando lista de posts...")
    resp = requests.get(BLOG_INDEX_URL)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    links = soup.select("ul.blog-posts li a")
    posts = []
    for link in links:
        href = link.get("href")
        titulo = link.get_text(strip=True)
        if href and not href.startswith("#"):
            posts.append({
                "url": urljoin(BLOG_INDEX_URL, href),
                "titulo": titulo,
            })
    print(f"✅ Encontrados {len(posts)} posts.")
    return posts


def extrair_conteudo(url):
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    titulo_elem = soup.find("h1") or soup.find("title")
    titulo = titulo_elem.get_text(strip=True) if titulo_elem else "Sem título"

    article = soup.find("article")
    if article:
        conteudo_html = str(article)
    else:
        body = soup.find("body")
        if body:
            for remover in body(["script", "nav", "footer", "header", "aside"]):
                remover.decompose()
            conteudo_html = str(body)
        else:
            raise ValueError("Não foi possível extrair o conteúdo.")

    return titulo, conteudo_html


def salvar_como_md(titulo, conteudo_html, url):
    nome_arquivo = slug_da_url(url) + ".md"
    caminho = os.path.join(PASTA_SAIDA, nome_arquivo)

    conteudo_md = conversor_md.handle(conteudo_html)

    cabecalho = f"""---
title: {titulo}
date: {datetime.now().strftime("%Y-%m-%d")}
source: {url}
description: ""
tags: []
---

"""

    with open(caminho, "w", encoding="utf-8") as f:
        f.write(cabecalho + conteudo_md)

    print(f"   💾 Salvo: {caminho}")


def main():
    posts = obter_links()
    erros = []

    for idx, post in enumerate(posts, 1):
        print(f"\n📄 [{idx}/{len(posts)}] {post['titulo']}")
        try:
            titulo, html = extrair_conteudo(post["url"])
            salvar_como_md(titulo, html, post["url"])
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            erros.append((post["url"], str(e)))

    print(f"\n✨ Pronto! {len(posts) - len(erros)}/{len(posts)} posts salvos em: {os.path.abspath(PASTA_SAIDA)}")
    if erros:
        print(f"\n⚠️  {len(erros)} erro(s):")
        for url, msg in erros:
            print(f"   {url} → {msg}")


if __name__ == "__main__":
    main()