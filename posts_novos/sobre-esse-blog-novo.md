---
title: Construí um Blog com uma API WebDAV e um Pouco de Python
date: 2026-05-10
slug: construi-um-blog-com-webdav-e-python
description: Como transformei o armazenamento de arquivos do Fastmail em um publicador de blog estático com 300 linhas de Python e nenhum pipeline de deploy.
tags: [python, web, fastmail, ferramentas]
---

Eu já pago pelo Fastmail. Pago pelo email, pelo calendário, pela sincronização de contatos, pelo domínio próprio. E em algum lugar nessa assinatura, quietinho, existe armazenamento de arquivos — acessível via WebDAV, servível por HTTP, apontado pro meu próprio domínio.

Isso é um servidor web. Eu já estava pagando por um servidor web e não sabia.

Então construí um blog nele.

## O problema com a maioria dos setups de sites estáticos

Já experimentei os suspeitos habituais. Hugo, Jekyll, Eleventy. São bons — software genuinamente bem feito — mas têm um custo que não é medido em dinheiro: têm um *pipeline*. Você escreve Markdown, roda um comando de build, faz push num repositório, alguma coisa faz o deploy. Existem arquivos de configuração. Existem temas com seus próprios arquivos de configuração. Existem dependências que quebram quando você atualiza o Node.

Não quero um pipeline. Quero escrever algo e que ele apareça na internet.

## O que o Fastmail realmente oferece

O Fastmail suporta vários protocolos abertos para acessar seus dados. Email via JMAP ou IMAP. Contatos via CardDAV. Arquivos — os relevantes aqui — via WebDAV.

WebDAV é antigo. É uma extensão do HTTP de 1996 que adiciona métodos como `MKCOL` (criar diretório) e `PROPFIND` (listar conteúdo de diretório). Toda conta Fastmail tem um endpoint WebDAV, e arquivos armazenados lá podem ser servidos diretamente por HTTP se você configurar seu domínio para apontá-los.

Essa é toda a infraestrutura.

## O script publish.py

O núcleo do sistema é um único arquivo Python — `publish.py` — que faz três coisas:

1. Parseia um arquivo Markdown com frontmatter YAML
2. Renderiza em um HTML autocontido com CSS embutido
3. Faz upload para o Fastmail via WebDAV

```python
python publish.py meu-post.md
```

Esse é o comando de deploy inteiro. Sem etapa de build. Sem git push. Sem CI/CD. Um comando, um arquivo na internet.

O frontmatter é mínimo:

```yaml
---
title: Título do Post
date: 2026-05-10
slug: titulo-do-post
description: Uma frase sobre o post.
tags: [python, ferramentas]
---
```

Todos os campos são opcionais. Se você omitir o título, ele deriva um do nome do arquivo. Se omitir a data, usa hoje. Se omitir o slug, slugifica o título. Você pode escrever um post sem nenhum frontmatter e ele ainda vai publicar corretamente.

## Estrutura no servidor

Cada post vive no seu próprio diretório, então as URLs ficam limpas:

```
blog/
├── index.html              ← listagem paginada de posts
├── page/2/index.html       ← posts mais antigos
├── search/index.html       ← página de busca
├── search.json             ← índice de busca (carregado por JS)
├── meu-post/
│   └── index.html
└── outro-post/
    └── index.html
```

O índice é reconstruído automaticamente a cada publicação. A paginação é estática — sem JavaScript para navegação, apenas páginas HTML pré-geradas. A busca, por outro lado, usa JavaScript: uma chamada `fetch` que carrega o `search.json` e filtra em tempo real enquanto você digita. Sem biblioteca de busca externa, sem backend.

## O scraper

Esse blog tem uma história. Escrevi coisas antes — espalhadas por um setup anterior — e queria trazer tudo sem fazer na mão.

Então, antes do publicador, escrevi um scraper:

```python
python scraper.py posts/
```

Ele acessa a página de índice do blog antigo, encontra todos os links de posts, busca cada um, extrai o conteúdo, converte o HTML para Markdown com `html2text`, e salva cada arquivo com um slug derivado da URL — não do título, porque a extração de título era instável e eu ficava com quinze arquivos com o mesmo nome.

Depois um script pequeno, `fix_titles.py`, corrigiu o frontmatter lendo o primeiro `# Título` no corpo de cada arquivo e usando isso como título canônico.

Três scripts, talvez 400 linhas no total. Migração feita.

## O que aprendi

**WebDAV é subestimado.** Não é glamouroso, não aparece em nenhum tutorial, mas funciona em todo lugar, não exige software de servidor especial, e a autenticação é só HTTP Basic — usuário e uma senha de aplicativo. O endpoint WebDAV do Fastmail respondeu corretamente a cada requisição na primeira tentativa.

**Estático é o padrão certo.** Cada funcionalidade dinâmica que adicionei a sites ao longo dos anos virou uma dívida de manutenção. Bancos de dados precisam de backup. Servidores precisam de atualização. Dependências se acumulam. Uma pasta de arquivos HTML não tem esses problemas. Uma pasta de arquivos HTML vai funcionar daqui a trinta anos.

**Controlar sua infraestrutura importa.** Não estou na plataforma de publicação de outra pessoa. Meus posts não estão sujeitos a uma mudança nos termos de serviço, uma reestruturação de preços ou um anúncio de descontinuação. Os arquivos vivem na minha conta do Fastmail, que eu controlo, apontados para o meu domínio, que eu possuo.

O índice de busca é um arquivo JSON. Os posts são HTML. Os estilos estão embutidos em cada arquivo. Se o Fastmail desaparecesse amanhã, eu poderia pegar os arquivos, colocar em qualquer lugar que sirva HTTP, e nada quebraria.

## O que falta

Não tem hospedagem de imagens — imagens precisam ser enviadas separadamente pela interface web do Fastmail ou via outra chamada WebDAV. Não tem feed RSS, embora seja uma adição pequena: gerar `feed.xml` junto com `index.html` durante a reconstrução do índice.

Não tem seção de comentários, e não tenho certeza se quero uma.

Não tem analytics, e tenho certeza que não quero.

## O ponto

Escrevi esse sistema numa tarde, depurando o URL do WebDAV na maior parte do tempo. O resultado é um blog que não custa nada a mais para rodar, faz deploy com um único comando, não tem pipeline de build, não tem dependências além de três pacotes Python, e vive numa infraestrutura que já era minha.

Isso parece certo.
