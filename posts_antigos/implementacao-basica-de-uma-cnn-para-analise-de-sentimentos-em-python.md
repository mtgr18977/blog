---
title: Implementação Básica de uma CNN para Análise de Sentimentos em Python
date: 2026-05-06
source: https://herebedragons.com.br/implementacao-basica-de-uma-cnn-para-analise-de-sentimentos-em-python/
description: ""
tags: []
---

# Implementação Básica de uma CNN para Análise de Sentimentos em Python

_ 10 Jul, 2024  _

**E se** se eu resolvesse, de formam mambembe, implementar uma CNN em Python com ajuda do ChatGPT?

Ficou assim.

### 1\. Instalar as Bibliotecas Necessárias

Certifique-se de ter o TensorFlow e Keras instalados em seu ambiente. Eles podem ser instalados usando o seguinte comando:
    
    
    pip install tensorflow
    

### 2\. Importar as Bibliotecas

No início do seu script Python, importe as bibliotecas necessárias:
    
    
    import numpy as np
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dense
    from tensorflow.keras.datasets import imdb
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    

## 3\. Carregar e Preparar os Dados

Carregue o conjunto de dados IMDb e prepare as sequências de texto:
    
    
    # Definir parâmetros
    max_features = 5000  # Número máximo de palavras
    max_len = 500  # Tamanho máximo de cada texto
    
    # Carregar o conjunto de dados IMDb
    (X_train, y_train), (X_test, y_test) = imdb.load_data(num_words=max_features)
    
    # Preencher ou truncar as sequências para o mesmo comprimento
    X_train = pad_sequences(X_train, maxlen=max_len)
    X_test = pad_sequences(X_test, maxlen=max_len)
    

### 4\. Construir o Modelo da CNN

Defina a arquitetura da rede neural convolucional:
    
    
    model = Sequential()
    model.add(Embedding(input_dim=max_features, output_dim=128, input_length=max_len))
    model.add(Conv1D(filters=64, kernel_size=5, activation='relu'))
    model.add(GlobalMaxPooling1D())
    model.add(Dense(10, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    

### 5\. Compilar o Modelo

Compile o modelo configurando o otimizador, a função de perda e as métricas de avaliação:
    
    
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    

### 6\. Treinar o Modelo

Treine o modelo com os dados de treino:
    
    
    model.fit(X_train, y_train, epochs=5, batch_size=32, validation_split=0.2)
    

### 7\. Avaliar o Modelo

Avalie o modelo usando os dados de teste:
    
    
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f'Test Accuracy: {accuracy:.2f}')
    

## Apêndice: Glossário de Termos

### Rede Neural Convolucional (CNN)

Um tipo de rede neural projetada para processar dados com uma estrutura de grade, como imagens ou sequências de texto.

### Embedding

Uma técnica para converter palavras em vetores densos de tamanho fixo que capturam relações semânticas entre as palavras.

### Conv1D

Uma camada de convolução unidimensional que aplica filtros sobre as sequências de entrada.

### GlobalMaxPooling1D

Uma camada de pooling que reduz a dimensionalidade ao selecionar o valor máximo de cada filtro.

### Dense

Uma camada totalmente conectada onde cada neurônio recebe entrada de todos os neurônios da camada anterior.

### Sigmoid

Uma função de ativação que transforma a saída em um valor entre 0 e 1, usada para tarefas de classificação binária.

### Adam

Um algoritmo de otimização que ajusta os pesos da rede neural de forma eficiente.

### Binary Crossentropy

Uma função de perda utilizada em problemas de classificação binária, medindo a diferença entre a saída prevista e a saída real.

### Batch Size

O número de amostras processadas antes de atualizar o modelo.

### Epoch

Uma única passagem por todo o conjunto de dados de treino.

## Referências

  1. Chollet, F. (2018). _Deep Learning with Python_. Manning Publications.
  2. Goodfellow, I., Bengio, Y., & Courville, A. (2016). _Deep Learning_. MIT Press.
  3. Géron, A. (2019). _Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow_. O'Reilly Media.
  4. Brownlee, J. (2018). _Deep Learning for Natural Language Processing_. Machine Learning Mastery.
  5. LeCun, Y., Bengio, Y., & Hinton, G. (2015). Deep learning. _Nature_ , 521(7553), 436-444.
  6. Olah, C. (2015). Understanding Convolutional Neural Networks. _colah's blog_.
  7. Raschka, S., & Mirjalili, V. (2017). _Python Machine Learning_. Packt Publishing.
  8. Srivastava, N., Hinton, G., Krizhevsky, A., Sutskever, I., & Salakhutdinov, R. (2014). Dropout: A simple way to prevent neural networks from overfitting. _Journal of Machine Learning Research_ , 15(1), 1929-1958.
  9. Goldberg, Y. (2017). Neural Network Methods for Natural Language Processing. _Synthesis Lectures on Human Language Technologies_ , 10(1), 1-309.
  10. Maas, A. L., Daly, R. E., Pham, P. T., Huang, D., Ng, A. Y., & Potts, C. (2011). Learning word vectors for sentiment analysis. In _Proceedings of the 49th Annual Meeting of the Association for Computational Linguistics: Human Language Technologies_.


