---
title: Projetos de final de semana - docs-cli
date: 2026-05-06
source: https://herebedragons.com.br/projetos-de-final-de-semana-docs-cli/
description: ""
tags: []
---

# Projetos de final de semana - docs-cli

_ 01 Jun, 2025  _

![Screenshot 2025-06-01 202856](https://bear-images.sfo2.cdn.digitaloceanspaces.com/paulogpd/screenshot-2025-06-01-202856.webp)

Eu trabalho diariamente com documentação e na minha formação acadêmica eu venho um background de linguística computacional. Isso quer dizer que eu gosto de ficar mexendo com texto, basicamente.

O que vem bem a calha com a nova onda de IA. Tokens, PoS, corpus/corpora, base terminológica, combinatórias léxicas, n-gramas, etc. Tudo isso foi o meu dia-a-dia de 2012 até 2016, quando eu atuava como bolsista na faculdade no Termisul e lutava diariamente com o Python para gerar um monte de XML que serviria de base pro meu robô de previsões terminológicas. Época pré-transformers.

Dito isso, hgoje eu sou redator técnico e tenho sempre a preocupação de manter a qualidade e a conformidade do que eu escrevo. Usar apenas a minha cabeça não é confiável - eu me esqueço de muita coisa - e fazer revisÕes manuais nem sempre é produtivo. Sem falar que é **muito** cansativo.

Assim, eu resolvi usar meu final de semana para criar uma ferramenta que analisa documentações (pode ser do tamanho que for) e tenta entender como melhorar essas documentações.

## Como funciona?

De forma básica, você primeiro baixa todos os documentos que deseja analisar, mantenha-os em formato markdown (`.md`). Se não tiver, transforme-os a partir do [html](https://codebeautify.org/html-to-markdown) ou do [PDF](https://openl.io/pt/pdf-to-markdown). Você também vai precisar uma chave de API do Google Gemini. Pode conseguir [uma grátis aqui](https://ai.google.dev/gemini-api/docs/api-key?hl=pt-br).

> Nunca exponha a sua chave de API na web ou faça coomit dela no GitHub. Use um arquivo `.env` para guardá-la ou adicione ela como uma variável de ambiente usando o comando `docs-cli api <sua chave>`.

Depois você o `docs-cli merge` para juntar todos os documentos em um único arquivo. Então você extraí as informações usando o comando `docs-cli extract`. Assim você vai ter um índice em formato `.json` que servirá para criar o embeddings. Para criar esses embeddings (explicação do que é ao final) você precisará usar o comando `docs-cli generate_embeddings`. Esse processo leva tempo, dependendo de quantos _chunks_ você vai usar e de quantos documentos (ou do quão grande é o seu arquivo de documentação consolidado), pode levar até um dia inteiro. No meu programa eu escolhi chunks que espelham a seção do markdown. Porque? porque, normalmente, cada seção tem o seu sentido próprio e inteiro, sem depende de outras, o que torna mais fácil analisar depois.

## Como usar?

Você poderá usar de 3 modos principais os resultados da sua documentação (os embeddings):

  1. **Análise de cobertura** : para fazer uma análise cobertura você vai precisar de um arquivo `.csv` que tenha duas colunas: `question` e `response`. É bom chamar o parâmetro `docs-cli clean_csv` antes, para se certificar de que o arquivo vai estar mais limpo possível. Mas o ideal ainda é que esse arquivo seja montado a partir de questões e respostas ideais, com as respostas vindas de um especialista. Após, rode `docs-cli evaluate` passando o arquivo CSV e o arquivo de embeddings. Esse script vai "bater" os seus documentos de acordo com as perguntas e procurar elas no seu corpus, gerando um percentual de cobertura para cada questão. Finalmente, você poderá gerar um relatório em HTML rodando `docs-cli report_html` ou um relatório em markdown rodando `docs-cli report_md`.



> Ao usar o parâmetro `clean_csv` você vai limpar ruídos comuns quando exportamos de plataformas de suporte e de Q&A, como "menu dropdown" ou "select + or -" entre outras. Mas é possível modificar esses parâmetros no código.

  2. **Rodar um assistente** : é possível rodar um assistente que responderá às suas questões de acordo com o que ele encontrar na sua documentação. Isso serve para uma análise mais detalhada por parte de um analista humano que, ao ver as respostas e as referências, poderá decidir o quão aderente está a resposta.

  3. **Gerador de documentos** : com essa base de conhecimento alimentado, limpa e indexada, você poderá criar um gerador de rascunhos de documentação. Aqueles longos guias podem ser gerados em pouco tempo usando os padrões anteriores de documentos. Fica mais refinado usando os seus próprios embeddings do que os do modelo de LLM.




## Onde acessar?

Eu publiquei o código-fonte sob a licença MIT (código aberto) no gituhub > <https://github.com/mtgr18977/docs-cli-toolkit>

Se você quiser apenas instalar e testar (e reportar bugs, por favor), pode usar o `pip` rodando o comando `pip install docs-cli-toolkit`.

A página no PIP fica aqui > <https://pypi.org/project/docs-cli-toolkit/>.

Qualquer coisa, pode abrir uma PR ou issue no GitHub. Ou me mandar um e-mail em paulo[at]paulogpd.com.br.
