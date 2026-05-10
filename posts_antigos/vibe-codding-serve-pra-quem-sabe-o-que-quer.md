---
title: Vibe codding serve pra quem sabe o que quer
date: 2026-05-06
source: https://herebedragons.com.br/vibe-codding-serve-pra-quem-sabe-o-que-quer/
description: ""
tags: []
---

# Vibe codding serve pra quem sabe o que quer

_ 09 Jul, 2025  _

Acho que foi esse ano ainda que o termo _vibe codding_ ganhou o mercado de tecnologia. A ideia é que uma pessoa programe usando linguagem natural com algum LLM do mercado. Algo como você pedir para o ChatGPT criar uma página web interativa para quye você possa acompanhar a sua vida financeira.

Isso funciona (sou a prova disso) quando a pessoa que "opera" o LLM sabe o quer e, principalmente, entende de desenvolvimento de software minimamente (ou seja, sabe a lógica por trás dos erros, sabe usar o console do navegador, sabe identificar loops e gaps que a IA está presa e coinsegue direcioná-la para sair dessas armadilhas).

Eu sempre soube o que fazer (lógica e ideia) mas nunca soube como fazer (me faltou, sempre, a capacidade manter a informação sobre a sintaxe das linguagens, suas particularidades, a melhor implementação etc). Assim, comigo, que já fui programador priscas eras atrás, o vibe codding melhora a minha vida. Eu consigo criar um tocador de MP3 com dois prompts. Consigo criar uma loja com algumas interações como v0 da Vercel. E, o principal, caso dê erro ou a IA fique presa, eu consigo debugar e direcionar a IA para arrumar o problema.

Como exercicio eu fiz isso hoje. Pedi para o ChatGPT-4o criar um script de análise de sentimentos de documentação técnica. E deu certo. Abaixo tem todo o processo.

* * *

**Instruções concisas que descrevem a tarefa**  
Descrever como realizar uma análise de sentimento em uma base de documentação técnica extensa e avaliar a utilidade prática dessa abordagem nesse contexto.

**Detalhes adicionais**  
A análise de sentimento, tradicionalmente aplicada a textos opinativos como reviews ou redes sociais, classifica textos como positivos, negativos ou neutros. A aplicação desse tipo de análise em documentação técnica precisa ser cuidadosamente interpretada, pois o objetivo desses documentos é geralmente informativo, não emocional.

* * *

## Vibe codding :)

### Etapas [opcional]

#### 1\. **Pré-processamento dos documentos**

  * Remova blocos de código, exemplos YAML/JSON, outputs e headers automáticos.
  * Mantenha apenas o conteúdo redacional.
  * Divida os documentos em blocos menores (parágrafos ou seções).



#### 2\. **Escolha do modelo de análise de sentimento**

  * Utilize modelos pré-treinados como:
    * `cardiffnlp/twitter-roberta-base-sentiment`
    * `distilbert-base-uncased-finetuned-sst-2-english`
    * Modelos multiclasse ou multilabel, se precisar distinguir tom informativo, erro crítico, alerta, sucesso etc.
  * Alternativamente, crie um modelo customizado com fine-tuning baseado em um dataset anotado com categorias relevantes para documentação técnica (ver abaixo).



#### 3\. **Execução da análise**

  * Aplique o modelo sobre os blocos preparados.
  * Armazene os resultados com metadados: nome do arquivo, parágrafo, categoria, pontuação de sentimento.



#### 4\. **Agrupamento e visualização**

  * Consolide os resultados em gráficos ou dashboards.
  * Filtre por:
    * Documentos com maior carga negativa.
    * Blocos com termos mais ambíguos ou conflitantes.
    * Diferenças por idioma ou por versão.



* * *

### Utilidade prática

#### ✅ _Casos em que a análise de sentimento pode ser útil na documentação técnica:_

  * **Detecção de linguagem ambígua ou alarmista** : termos como “fatal”, “erro grave”, “problema crítico” usados fora de contexto podem gerar interpretações equivocadas.
  * **Auditoria de tom e consistência** : garante que a documentação mantenha um tom neutro, impessoal e instrucional.
  * **Feedback automático** : identificar pontos que soem duros ou confusos para usuários finais (especialmente útil se combinada com feedback de suporte técnico).
  * **Monitoramento de mudanças** : rastrear quando atualizações introduzem linguagem mais negativa ou confusa do que versões anteriores.



#### ❌ _Casos em que pode ser irrelevante ou gerar ruído:_

  * Documentos puramente estruturais ou de referência (ex: schemas de API).
  * Textos que contêm muitos trechos técnicos (blocos de código, logs).
  * Alto risco de falso positivo (ex: “erro” sendo descrito corretamente, mas classificado como negativo).



### Formato de saída

  * Idealmente: CSV ou JSON com os seguintes campos:


    
    
    [
      {
        "document": "file_name.md",
        "section": "Introduction",
        "text": "If this error occurs, restart the agent...",
        "sentiment": "Negative",
        "confidence": 0.87
      }
    ]
    

  * Dashboard opcional em HTML/JS ou ferramenta como Power BI/Streamlit, com filtros por tipo de sentimento, trecho e documento.



### Exemplos [opcional]

**Entrada**
    
    
    If this error occurs, you must restart the system immediately. This can cause service downtime.
    

**Saída esperada**
    
    
    {
      "sentiment": "Negative",
      "confidence": 0.91
    }
    

**Entrada**
    
    
    You can use the `--force` flag to override the default behavior.
    

**Saída esperada**
    
    
    {
      "sentiment": "Neutral",
      "confidence": 0.96
    }
    

* * *

**Instruções concisas que descrevem a tarefa**  
Implementar um script Python que execute análise de sentimento em arquivos `.md` de documentação técnica, utilizando modelos da biblioteca `transformers`. O script deve ler todos os arquivos Markdown de uma pasta, dividir em parágrafos, aplicar a análise de sentimento e exportar os resultados em formato `.json`.

* * *

### Etapas [opcional]

  1. Pré-requisitos:

     * Python 3.8+
     * Biblioteca `transformers`
     * Biblioteca `torch`
     * Diretório com arquivos `.md` organizados
  2. Instalação de dependências:



    
    
    pip install transformers torch
    

  3. Estrutura de pastas esperada:


    
    
    sentiment_analyzer/
    ├── docs/
    │   ├── file1.md
    │   └── subfolder/
    │       └── file2.md
    ├── analyze_sentiment.py
    

* * *

### Formato de saída

  * Arquivo `sentiment_results.json`, com a estrutura:


    
    
    [
      {
        "document": "file1.md",
        "text": "This command may fail if the server is unreachable.",
        "sentiment": "NEGATIVE",
        "confidence": 0.8743
      },
      ...
    ]
    

* * *

### Código do script: `analyze_sentiment.py`
    
    
    import os
    import json
    import glob
    from transformers import pipeline
    
    # Caminho para os arquivos Markdown
    DOCS_FOLDER = "docs"
    OUTPUT_FILE = "sentiment_results.json"
    
    # Carregar o pipeline de análise de sentimento
    analyzer = pipeline("sentiment-analysis")
    
    def get_paragraphs(content):
        # Divide por parágrafos (blocos separados por linha em branco)
        return [p.strip() for p in content.split("\n\n") if len(p.strip()) > 20]
    
    def analyze_markdown_files():
        results = []
        for filepath in glob.glob(os.path.join(DOCS_FOLDER, "**/*.md"), recursive=True):
            with open(filepath, encoding="utf-8") as f:
                content = f.read()
            paragraphs = get_paragraphs(content)
            for para in paragraphs:
                analysis = analyzer(para[:512])[0]  # truncar se for longo
                results.append({
                    "document": os.path.relpath(filepath, DOCS_FOLDER),
                    "text": para,
                    "sentiment": analysis["label"],
                    "confidence": float(round(analysis["score"], 4))
                })
        with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
            json.dump(results, out, indent=2, ensure_ascii=False)
        print(f"\nAnálise concluída. Resultados salvos em: {OUTPUT_FILE}")
    
    if __name__ == "__main__":
        analyze_markdown_files()
    

* * *

### Como usar

  1. Crie uma pasta chamada `sentiment_analyzer`.
  2. Coloque os arquivos `.md` dentro de uma subpasta chamada `docs`.
  3. Salve o script acima como `analyze_sentiment.py`.
  4. Instale as dependências:


    
    
    pip install transformers torch
    

  5. Execute:


    
    
    python analyze_sentiment.py
    

* * *

### Exemplos [opcional]

**Entrada (exemplo de`.md`):**
    
    
    ## Troubleshooting
    
    If the agent fails to start, restart the server manually.
    
    ## Logging
    
    All events are logged to /var/log/app.log for later inspection.
    

**Saída (trecho do`.json`):**
    
    
    [
      {
        "document": "troubleshooting.md",
        "text": "If the agent fails to start, restart the server manually.",
        "sentiment": "NEGATIVE",
        "confidence": 0.9123
      }
    ]
    

**Instruções concisas que descrevem a tarefa**  
Adaptar o script Python de análise de sentimento para gerar dois formatos adicionais de saída: um arquivo `.csv` com os resultados e um dashboard HTML interativo para visualização dos dados por sentimento, documento e confiança.

* * *

### Etapas [opcional]

#### 1\. Continuação do script principal (`analyze_sentiment.py`)

Adicione duas exportações:

  * `sentiment_results.csv` com colunas: `document`, `sentiment`, `confidence`, `text`
  * `dashboard.html` com uma visualização de filtros (por sentimento, por documento, ordenação por confiança)



* * *

### Formato de saída

**CSV:**
    
    
    document,sentiment,confidence,text
    guide/intro.md,POSITIVE,0.991,"You can use this method safely."
    guide/errors.md,NEGATIVE,0.823,"This may result in failure if misconfigured."
    

**HTML interativo:** Tabela com:

  * Filtros dropdown para `sentiment` e `document`
  * Campo de busca por texto
  * Ordenação por `confidence`



* * *

### Código atualizado: `analyze_sentiment.py`
    
    
    import os
    import json
    import glob
    import csv
    from transformers import pipeline
    
    DOCS_FOLDER = "docs"
    JSON_FILE = "sentiment_results.json"
    CSV_FILE = "sentiment_results.csv"
    HTML_FILE = "dashboard.html"
    
    analyzer = pipeline("sentiment-analysis")
    
    def get_paragraphs(content):
        return [p.strip() for p in content.split("\n\n") if len(p.strip()) > 20]
    
    def analyze_markdown_files():
        results = []
        for filepath in glob.glob(os.path.join(DOCS_FOLDER, "**/*.md"), recursive=True):
            with open(filepath, encoding="utf-8") as f:
                content = f.read()
            paragraphs = get_paragraphs(content)
            for para in paragraphs:
                analysis = analyzer(para[:512])[0]
                results.append({
                    "document": os.path.relpath(filepath, DOCS_FOLDER),
                    "text": para,
                    "sentiment": analysis["label"],
                    "confidence": round(float(analysis["score"]), 4)
                })
    
        with open(JSON_FILE, "w", encoding="utf-8") as out:
            json.dump(results, out, indent=2, ensure_ascii=False)
    
        with open(CSV_FILE, "w", encoding="utf-8", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["document", "sentiment", "confidence", "text"])
            writer.writeheader()
            writer.writerows(results)
    
        generate_html_dashboard(results)
    
        print(f"Análise concluída. Arquivos salvos:\n- {JSON_FILE}\n- {CSV_FILE}\n- {HTML_FILE}")
    
    def generate_html_dashboard(results):
        with open(HTML_FILE, "w", encoding="utf-8") as f:
            f.write("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>Sentiment Dashboard</title>
      <style>
        body { font-family: sans-serif; padding: 20px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ccc; padding: 8px; }
        th { background-color: #eee; }
        input, select { padding: 4px; margin-right: 10px; }
      </style>
    </head>
    <body>
      <h1>Sentiment Analysis Dashboard</h1>
      <label>Filter by sentiment:
        <select id="sentimentFilter">
          <option value="">All</option>
          <option value="POSITIVE">Positive</option>
          <option value="NEGATIVE">Negative</option>
          <option value="NEUTRAL">Neutral</option>
        </select>
      </label>
      <label>Filter by document:
        <select id="documentFilter">
          <option value="">All</option>
        </select>
      </label>
      <label>Search:
        <input type="text" id="searchInput" placeholder="Search text...">
      </label>
      <table id="dataTable">
        <thead>
          <tr>
            <th>Document</th>
            <th>Sentiment</th>
            <th>Confidence</th>
            <th>Text</th>
          </tr>
        </thead>
        <tbody></tbody>
      </table>
    <script>
      const data = %s;
    
      const sentimentFilter = document.getElementById("sentimentFilter");
      const documentFilter = document.getElementById("documentFilter");
      const searchInput = document.getElementById("searchInput");
      const tbody = document.querySelector("#dataTable tbody");
    
      const documents = [...new Set(data.map(row => row.document))];
      documents.forEach(doc => {
        const opt = document.createElement("option");
        opt.value = doc;
        opt.textContent = doc;
        documentFilter.appendChild(opt);
      });
    
      function renderTable() {
        const sentiment = sentimentFilter.value;
        const document = documentFilter.value;
        const query = searchInput.value.toLowerCase();
        tbody.innerHTML = "";
        data.filter(row => {
          return (!sentiment || row.sentiment === sentiment)
              && (!document || row.document === document)
              && (!query || row.text.toLowerCase().includes(query));
        }).forEach(row => {
          const tr = document.createElement("tr");
          tr.innerHTML = `
            <td>${row.document}</td>
            <td>${row.sentiment}</td>
            <td>${row.confidence}</td>
            <td>${row.text.replace(/</g, "&lt;")}</td>`;
          tbody.appendChild(tr);
        });
      }
    
      sentimentFilter.onchange = renderTable;
      documentFilter.onchange = renderTable;
      searchInput.oninput = renderTable;
    
      renderTable();
    </script>
    </body>
    </html>
    """ % json.dumps(results))
    

* * *

### Como usar

  1. Execute o script após colocar os `.md` em `docs/`.
  2. Arquivos gerados:
     * `sentiment_results.json`: dados brutos
     * `sentiment_results.csv`: para uso em Excel, Power BI, etc.
     * `dashboard.html`: abra em qualquer navegador para filtrar e explorar



* * *

**Instruções concisas que descrevem a tarefa**  
Incorporar gráficos interativos ao dashboard HTML gerado pela análise de sentimento em documentação técnica. O dashboard deve permitir visualização por distribuição de sentimentos e confiança, utilizando a biblioteca Chart.js.

* * *

### Etapas [opcional]

  1. Integrar o carregamento de dados no JavaScript embutido.
  2. Utilizar a [Chart.js](https://www.chartjs.org/) via CDN.
  3. Criar:
     * Gráfico de pizza (`pie chart`) para mostrar proporção de sentimentos.
     * Gráfico de barras horizontais (`bar chart`) para média de confiança por tipo de sentimento.



* * *

### Formato de saída

O arquivo `dashboard.html` terá:

  * Filtros interativos por sentimento, documento e texto
  * Gráficos:
    * **Pizza:** Proporção de sentimentos (Positive, Negative, Neutral)
    * **Barras:** Confiança média por sentimento



* * *

### Trecho adicional a ser incluído no HTML

Insira este conteúdo no `<body>` antes da `<table>`:
    
    
    <canvas id="pieChart" height="200"></canvas>
    <canvas id="barChart" height="200"></canvas>
    

E logo **antes do fechamento de`</body>`**, adicione:
    
    
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
      const ctxPie = document.getElementById('pieChart').getContext('2d');
      const ctxBar = document.getElementById('barChart').getContext('2d');
    
      const countBySentiment = {};
      const sumConfidence = {};
    
      data.forEach(row => {
        const s = row.sentiment;
        countBySentiment[s] = (countBySentiment[s] || 0) + 1;
        sumConfidence[s] = (sumConfidence[s] || 0) + row.confidence;
      });
    
      const sentiments = Object.keys(countBySentiment);
      const counts = sentiments.map(s => countBySentiment[s]);
      const avgConfidence = sentiments.map(s => (sumConfidence[s] / countBySentiment[s]).toFixed(2));
    
      new Chart(ctxPie, {
        type: 'pie',
        data: {
          labels: sentiments,
          datasets: [{
            label: 'Sentiment Distribution',
            data: counts,
            backgroundColor: ['#4ade80', '#f87171', '#60a5fa']
          }]
        }
      });
    
      new Chart(ctxBar, {
        type: 'bar',
        data: {
          labels: sentiments,
          datasets: [{
            label: 'Average Confidence',
            data: avgConfidence,
            backgroundColor: '#a78bfa'
          }]
        },
        options: {
          indexAxis: 'y',
          scales: {
            x: {
              min: 0,
              max: 1
            }
          }
        }
      });
    </script>
    

* * *

E no final, ele gerou um arquivo `.zip` com tudo o que foi feito.  


**Resumo** : sabendo usar, você consegue programar usando linguagem natural. Talvez isso vire um paradigma? Talvez. Para quem fala da complexidade, é bom lembrar que nos anos 70 as pessopas utilizavam C, Cobol e outras linguagens que não tinham nada implementado por padrão, hoje, a maioria do trabalho de um desenvolvedor (JR/PL) vai ser realizar a interconexão de diversas bibliotecas, bases de dados e outras ferramentas qwue já foram feitas por outras pessoas.
