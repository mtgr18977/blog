# fastmail-blog

Um sistema de blog estático minimalista que publica posts em Markdown diretamente no **Fastmail Files** via WebDAV. Sem etapa de build, sem servidor, sem framework — só Python e sua escrita.

---

## Como funciona

```
Arquivo Markdown (.md)
        ↓
   publish.py
        ↓
Página HTML (com CSS embutido)
        ↓
Fastmail WebDAV (seu domínio)
```

Os posts são convertidos de Markdown para páginas HTML autocontidas e enviados para o armazenamento do Fastmail Files, que pode ser servido como site estático pelo seu domínio personalizado.

---

## Requisitos

- Python 3.10+
- Conta no [Fastmail](https://fastmail.com) com Files & Storage ativado
- Domínio personalizado apontado para o Fastmail (opcional, mas recomendado)

Instale as dependências:

```bash
pip install requests markdown pyyaml
```

Ou com `uv`:

```bash
uv pip install requests markdown pyyaml
```

---

## Configuração

**1. Copie o template de configuração:**

```bash
cp .blog-config.example.json .blog-config.json
```

**2. Preencha suas credenciais:**

```json
{
  "webdav_base_url": "https://myfiles.fastmail.com/",
  "webdav_username": "voce@fastmail.com",
  "webdav_app_password": "SUA_APP_PASSWORD",
  "blog_path": "blog/",
  "site_title": "Meu Blog",
  "site_description": "Uma descrição curta",
  "author": "Seu Nome",
  "base_url": "https://seudominio.com/blog/",
  "posts_per_page": 10
}
```

Para gerar uma app password no Fastmail: **Settings → Privacy & Security → Manage app passwords**

Para encontrar sua URL WebDAV: **Settings → Files & Storage**

> `.blog-config.json` está no `.gitignore` — nunca commite suas credenciais.

---

## Escrevendo posts

Posts são arquivos Markdown com frontmatter YAML:

```markdown
---
title: Meu primeiro post
date: 2024-01-15
description: Um resumo curto exibido no índice.
tags: [escrita, pessoal]
---

Seu conteúdo aqui.
```

| Campo         | Obrigatório | Descrição                                    |
|---------------|-------------|----------------------------------------------|
| `title`       | Não         | Padrão: nome do arquivo                      |
| `date`        | Não         | Padrão: data de hoje                         |
| `description` | Não         | Exibido no índice de posts                   |
| `tags`        | Não         | Lista ou string separada por vírgulas        |
| `slug`        | Não         | Slug da URL; gerado automaticamente do título|

Extensões Markdown suportadas: blocos de código com sintaxe, tabelas, notas de rodapé, sumário automático, highlight de código.

---

## Publicando

```bash
# Publicar um único post
python publish.py meu-post.md

# Reconstruir o índice completo (após editar vários posts)
python publish.py --rebuild-index

# Listar todos os posts publicados
python publish.py --list

# Deletar um post pelo slug
python publish.py --delete slug-do-post
```

---

## Importando posts existentes

O `scrap_blog.py` faz scraping de um blog existente e salva cada post como arquivo Markdown compatível com o `publish.py`:

```bash
# Salvar no diretório atual
python scrap_blog.py

# Salvar em uma pasta específica
python scrap_blog.py posts_antigos/
```

Edite a variável `BLOG_INDEX_URL` dentro do script para apontar para o blog de origem.

---

## Estrutura de diretórios

```
.
├── publish.py                # Publicador principal
├── scrap_blog.py             # Scraper / importador de blog
├── .blog-config.json         # Suas credenciais (no gitignore)
├── .blog-config.example.json
├── .blog-posts.json          # Registro local de posts (gerenciado automaticamente)
├── preview-index.html        # Prévia local da página de índice
├── preview-post.html         # Prévia local de um post
├── posts_antigos/            # Posts importados / arquivados
└── posts_novos/              # Novos posts para publicar
```

---

## Design

O HTML gerado é autocontido com CSS embutido. O tema padrão usa:

- **Fontes**: Josefin Sans (títulos), Lora (corpo), JetBrains Mono (código)
- **Cores**: Fundo escuro (`#1a2332`) com detalhes em teal
- **Layout**: Coluna única, máximo de 720px, responsivo

Para personalizar o design, edite a constante `CSS` no `publish.py`.

---

## Licença

MIT
