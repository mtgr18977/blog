---
title: Brincando com dados - insights sobre o campeonato brasileiro
date: 2026-05-06
source: https://herebedragons.com.br/brincando-com-dados-insights-sobre-o-campeonato-brasileiro/
description: ""
tags: []
---

# Brincando com dados - insights sobre o campeonato brasileiro  
  
_ 24 Jun, 2025  _

Reuni todos os dados dos jogos do campeonato brasileiro de 2003 até 2025 (10 rodada). Primeiro utilizei o dataset [disponível aqui](https://www.kaggle.com/datasets/adaoduque/campeonato-brasileiro-de-futebol/data) feito pelo [Adão Duque](https://www.kaggle.com/adaoduque). Depois reuni, usando o ChatGPT 4.5, os dados das 10 primeiras rodadas de 2025 e reuni em um segundo dataset, [diponível aqui](https://www.kaggle.com/datasets/paulopilotti/br-2025). Este é bem simples (sem rodada e sem data) e serve apenas como balisador dos dados desse ano. Assim, tirei 0 pó do python e fui pra gerar algumas coisas que, um dia, podem ser interessantes.

**Primeiro** , o clube com maior crescimento de Elo no período analisado: **Palmeiras** (+172.08 pontos) o que bate muito bem com a evolução do clube da série B até o bicho papão da américa.

Depois, reuni algumas outras coisas:

### Percentual de vitórias como mandante

Clube mandante | %  
---|---  
Internacional | 0.586797  
Grêmio | 0.585052  
Palmeiras | 0.580311  
São Paulo | 0.574766  
Santos | 0.562347  
Flamengo | 0.550351  
Corinthians | 0.540342  
Cruzeiro | 0.533693  
Fluminense | 0.495327  
Vasco | 0.447447  
  
### Percentual de empates como visitante

Clube visitante | %  
---|---  
Corinthians | 0.300733  
Palmeiras | 0.300518  
Vasco | 0.294294  
São Paulo | 0.287383  
Flamengo | 0.284382  
Internacional | 0.281174  
Grêmio | 0.275773  
Santos | 0.271394  
Fluminense | 0.242991  
Cruzeiro | 0.22372  
  
### Confrontos grandes com maior desequilíbrio

Confronto | Diferença de gols  
---|---  
SPFC x Vasco | 1.41176  
Flamengo x Cruzeiro | 1.21053  
Grêmio x Vasco | 1.0625  
Santos x Vasco | 1.0625  
Grêmio x Flamengo | 1  
  
## Gráfico de evolução do Elo

![Figure_1](https://bear-images.sfo2.cdn.digitaloceanspaces.com/paulogpd/figure_1.webp)

* * *

# Previsão de Jogos - Modelo Híbrido Poisson + Elo

Mandante | Visitante | Gols Mandante | Gols Visitante | Prob Mandante (%) | Prob Empate (%) | Prob Visitante (%) | Palpite  
---|---|---|---|---|---|---|---  
Internacional | Vitoria | 1.82 | 0.76 | 62.6 | 22.3 | 15.1 | Mandante  
Bahia | Atletico Mineiro | 1.28 | 1.18 | 38.8 | 27.2 | 34 | Mandante  
Corinthians | Bragantino | 1.39 | 0.95 | 47.1 | 27.3 | 25.6 | Mandante  
Cruzeiro | Gremio | 1.55 | 1.02 | 49.5 | 25.5 | 25 | Mandante  
Fortaleza | Ceara | 1.37 | 0.89 | 47.9 | 27.6 | 24.5 | Mandante  
Juventude | Sport | 1.55 | 0.82 | 54.6 | 25.6 | 19.8 | Mandante  
Flamengo | Sao Paulo | 1.44 | 1.03 | 46.7 | 26.5 | 26.9 | Mandante  
Vasco | Botafogo | 1.32 | 1.15 | 40.7 | 27.1 | 32.3 | Mandante  
Santos | Palmeiras | 1.43 | 1.15 | 43.4 | 26.2 | 30.4 | Mandante  
Mirassol | Fluminense | 2.35 | 1.31 | 60.6 | 19.1 | 20.3 | Mandante  
  
* * *

## Resumo do que foi feito e do que o script faz

### Principais Funcionalidades

  * Cálculo de forças: determina as forças de ataque e defesa dos times quando jogam em casa ou fora, utilizando dados históricos de gols.
  * Vantagem de casa: avalia a vantagem de jogar em casa para cada time, ajustando os ratings de Elo com base no saldo médio de gols como mandante.
  * Previsão de resultados: utiliza a distribuição de Poisson para estimar a probabilidade de diferentes placares e, combinada com ajustes do rating Elo, prevê vencedores e chances de empate.
  * Atualização de ratings: após cada jogo, os ratings Elo são atualizados para refletir o resultado real, ajustando futuras previsões com maior precisão.



### Como Funciona

  * Dados de entrada: utiliza um DataFrame do pandas com informações sobre jogos anteriores (times mandante e visitante, gols marcados e sofridos).
  * Cálculo de métricas: calcula as forças de ataque/defesa, vantagens de casa e médias de gols da liga.
  * Modelo de previsão: combina essas métricas com um sistema de ajuste baseado no Elo para prever os resultados das partidas futuras.
  * Saída: fornece uma tabela de previsões com probabilidades e palpites, formatada em Markdown para fácil visualização.



**Nota técnica** : o código utiliza Python com bibliotecas `pandas` e `math`. Para rodar, é necessário ter um arquivo `CSV` com dados históricos de partidas, incluindo nomes dos times e gols marcados. As previsões são ajustadas dinamicamente conforme os resultados dos jogos são incorporados, atualizando os ratings Elo e melhorando a precisão ao longo do tempo.

**Nota do apostador** : não parece ser muito confiável apostar em todos os mandantes, uma vez que o esporte não é uma ciência exata. O modelo aponta eles como vencedores por uma série de fatores, contudo, se você analisar bem, alguns jogos tem as probabilidade (chances) muito próximas, o que indica um grande equilibrio.

* * *

O nome é em homenagem ao Saraiva, aka Sassá ou Sassamaru, meu cachorro vira-lata de 10 anos :)

Código no Github: <https://github.com/mtgr18977/sassamaru-br-25>
