# 📝 Blog Publisher Web Interface

Uma interface web para publicar posts no seu blog estático hospedado no Fastmail Files via WebDAV.

## Funcionalidades

- **Publicar posts**: Cole o conteúdo markdown completo (com frontmatter YAML) e publique diretamente no Fastmail
- **Preview**: Visualize como o markdown será renderizado antes de publicar
- **Configuração**: Configure suas credenciais do WebDAV através da interface
- **Gerenciar posts**: Veja a lista de posts publicados e delete quando necessário
- **Rebuild Index**: Recrie as páginas de índice do blog

## Instalação

```bash
pip install -r requirements.txt
```

## Uso

### 1. Iniciar a aplicação web

```bash
python app.py
```

A aplicação irá iniciar em `http://localhost:5000`

### 2. Configurar credenciais

Acesse `/config` e preencha:

- **WebDAV Base URL**: Geralmente `https://myfiles.fastmail.com/`
- **WebDAV Username**: Seu email do Fastmail
- **WebDAV App Password**: Senha de aplicativo gerada em Fastmail → Settings → Privacy & Security → Manage app passwords
- **Blog Path**: Caminho da pasta no Fastmail Files (ex: `blog/`)
- **Site Title**: Título do seu blog
- **Base URL**: URL pública onde seu blog estará disponível

### 3. Publicar um post

1. Acesse a página inicial (`/`)
2. Cole o conteúdo do arquivo markdown (incluindo o frontmatter YAML entre `---`)
3. Clique em "Preview" para visualizar
4. Clique em "🚀 Publicar no Fastmail"

### Formato do Markdown

O arquivo deve seguir o formato:

```markdown
---
title: Meu Post Incrível
date: 2024-01-15
description: Uma breve descrição do post
tags: python, blog, tutorial
---

Conteúdo do post em markdown...
```

A data também pode ser extraída automaticamente se estiver no corpo do texto no formato `_ 15 Jan, 2024 _`.

## Variáveis de Ambiente

- `PORT`: Porta para rodar a aplicação (padrão: 5000)
- `SECRET_KEY`: Chave secreta para sessões Flask (padrão: "dev-key-change-in-production")
- `FLASK_DEBUG`: Habilita modo debug (padrão: true)

## Exemplo com Docker

```bash
docker run -p 5000:5000 \
  -e SECRET_KEY="sua-chave-secreta" \
  -v ./config:/workspace/.blog-config.json \
  blog-publisher
```

## Segurança

⚠️ **Importante**: As credenciais do WebDAV são salvas em `.blog-config.json`. Em produção:

1. Use uma `SECRET_KEY` forte
2. Desabilite o modo debug (`FLASK_DEBUG=false`)
3. Use HTTPS através de um reverse proxy (nginx, traefik, etc.)
4. Considere usar autenticação na frente da aplicação

## Como Funciona

A aplicação web utiliza as mesmas funções do `publish.py` para:

1. Parsear o markdown e extrair frontmatter
2. Converter markdown para HTML
3. Renderizar o template HTML completo com CSS embutido
4. Upload via WebDAV para o Fastmail Files
5. Atualizar o registry de posts
6. Rebuild das páginas de índice

## Rotas da API

- `GET /` - Página de publicação
- `POST /publish` - Publicar um post
- `GET /config` - Página de configuração
- `POST /config/save` - Salvar configuração
- `GET /posts` - Lista de posts publicados
- `POST /posts/delete` - Deletar um post
- `GET /posts/rebuild-index` - Rebuild do índice
- `POST /api/preview` - Preview do markdown (JSON)

## Licença

MIT
