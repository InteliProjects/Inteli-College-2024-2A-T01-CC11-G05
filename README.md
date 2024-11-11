<table>
<tr>
<td>
<a href= "https://brastelnet.com.br/"><img src="./root/artigo/imgs/brastel-logo.png" alt="Brastel" border="0" width="100%"></a>
</td>
<td><a href= "https://www.inteli.edu.br/"><img src="./inteli-logo.png" alt="Inteli - Instituto de Tecnologia e Liderança" border="0" width="30%"></a>
</td>
</tr>
</table>

# Introdução

Este projeto consiste em um chatbot inteligente para a Brastel Co., com o objetivo de melhorar a comunicação e o atendimento ao cliente. Utilizando técnicas avançadas e Machine Learning, o chatbot é capaz de entender e responder a perguntas dos usuários de forma eficiente, facilitando o suporte e automatizando tarefas.


# Projeto: Implementação de um Chatbot para melhorar o atendimento do SAC.

# Grupo: G5

# Integrantes:

* [André Junior](<andre.junior@sou.inteli.edu.br>)
* [Arthur Reis](<arthur.reis@sou.inteli.edu.br>)
* [Jonas Sales](<jonas.sales@sou.inteli.edu.br>)
* [Luiz Gonçalves](<luiz.goncalves@sou.inteli.edu.br>)
* [Luiz Júnior](<luiz.junior@sou.inteli.edu.br>)
* [Mateus Silva](<mateus.silva@sou.inteli.edu.br>)
* [Vinicius Santos](<vinicius.santos@sou.inteli.edu.br>)

# Descrição

Este projeto faz parte de um esforço colaborativo de estudantes para desenvolver um chatbot inteligente para a Brastel, com o objetivo de melhorar a comunicação e o atendimento ao cliente. Utilizando técnicas avançadas de Processamento de Linguagem Natural (PLN) e Machine Learning, o chatbot é capaz de entender e responder a perguntas dos usuários de forma eficiente, facilitando o suporte e automatizando tarefas comuns.

Ao longo deste projeto, exploramos várias metodologias de desenvolvimento de chatbots, incluindo a criação de uma pipeline de dados, a construção de modelos de NLU (Natural Language Understanding), e a integração de algoritmos de aprendizado profundo para aprimorar a precisão das respostas. Nosso foco está em garantir que a solução seja escalável, fácil de usar e que ofereça uma experiência de alta qualidade para os clientes da Brastel.

Este repositório contém todos os recursos, código e documentação necessários para entender o desenvolvimento e o funcionamento do chatbot.

# Artigo

Os arquivos do artigo estão na pasta [/artigo](./root/artigo/artigo.md). 

O conteúdo deste artigo foi elaborado como parte das atividades de aprendizado dos alunos, mas precisa ser revisto e modificado caso haja a intenção de submetê-lo para uma eventual publicação.

# Configuração para desenvolvimento

## Instalações necessárias

**Para executar o projeto, você precisará instalar as seguintes ferramentas:**

- [Python 3.12](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/products/docker-desktop)
- [Git](https://git-scm.com/downloads)
- [Jupyter Notebook](https://jupyter.org/install) (opcional, pois pode ser executado no Google Colab)
- [Visual Studio Code](https://code.visualstudio.com/download) (opcional, mas recomendado)
- [React](https://reactjs.org/docs/getting-started.html) (opcional, para desenvolvimento do frontend)
- [JavaScript](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript) (opcional, para desenvolvimento do frontend)
- [FastAPI](https://fastapi.tiangolo.com/) (opcional, para desenvolvimento do backend)

## Configuração do ambiente

**Para configurar o ambiente de desenvolvimento, siga as instruções abaixo:**

1. Instale o Git no seu computador.
Para instalar o Git, acesse o site oficial e siga as instruções de instalação: [Git](https://git-scm.com/downloads)

2. Clone o repositório do projeto.
Para clonar o repositório, abra o terminal e execute o seguinte comando:

```bash
git clone <link-do-repositorio>
```

3. Instale o Visual Studio Code.
Para instalar o Visual Studio Code, acesse o site oficial e siga as instruções de instalação: [Visual Studio Code](https://code.visualstudio.com/download)

4. Instale o Python 3.12.
Para instalar o Python, acesse o site oficial e siga as instruções de instalação: [Python 3.12](https://www.python.org/downloads/). Certifique-se de adicionar o Python ao PATH durante a instalação.

5. Instale o Docker.
Para instalar o Docker, acesse o site oficial e siga as instruções de instalação: [Docker](https://www.docker.com/products/docker-desktop)

6. Instale o Jupyter Notebook (opcional).
Para instalar o Jupyter Notebook, acesse o site oficial e siga as instruções de instalação: [Jupyter Notebook](https://jupyter.org/install)

7. Instale o React (opcional).
Para instalar o React, acesse o site oficial e siga as instruções de instalação: [React](https://reactjs.org/docs/getting-started.html)

8. Instale o FastAPI (opcional).
Para instalar o FastAPI, acesse o site oficial e siga as instruções de instalação: [FastAPI](https://fastapi.tiangolo.com/). Certifique-se de instalar o FastAPI no ambiente virtual do Python.

9. Instale o JavaScript (opcional).
Para instalar o JavaScript, acesse o site oficial e siga as instruções de instalação: [JavaScript](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript)


## Execução do chatbot

**Para executar o projeto, siga as instruções abaixo:**

Com o ambiente configurado, você pode executar o projeto localmente ou em um ambiente de desenvolvimento.

**Para executar o projeto localmente, siga as instruções abaixo:**

1. Abra o Visual Studio Code e abra a pasta do projeto.

2. Abra o terminal do Visual Studio Code e execute o seguinte comando para instalar o docker-compose:

```bash
pip install docker-compose
```

3. Execute o seguinte comando para iniciar o projeto:

```bash
docker-compose up
```

4. Abra o navegador e acesse o seguinte endereço:

```bash
http://localhost:3000
```

5. Para parar o projeto, execute o seguinte comando:

```bash
docker-compose down
```

## Execução dos modelos NLU e NLG

**Para executar os modelos NLU e NLG, siga as instruções abaixo:**

**Opção 1: Executar no Google Colab**

1. Acesse o site do Google Colaboratory: [Google Colab](https://colab.research.google.com/) e faça login com sua conta do Google.

2. Faça o upload do arquivo do modelo NLU ou NLG que deseja executar.

3. Conecte o Google Colab ao ambiente de execução no canto superior direito da tela. Recomendado usar o ambiente de execução GPU.

4. Execute o código no Google Colab.


**Opção 2: Executar no Jupyter Notebook**

1. Abra o Jupyter Notebook no seu computador.

2. Abra o arquivo do modelo NLU ou NLG que deseja executar.

3. Execute as células de código no Jupyter Notebook.

**Opção 3: Executar no Visual Studio Code**

1. Abra o Visual Studio Code e abra a pasta do projeto.

2. Na seção de Extensões, instale a extensão do Jupyter Notebook.

3. Com a extensão instalada, abra o arquivo do modelo NLU ou NLG que deseja executar.

4. Execute as células de código no Jupyter Notebook.


# Licença

Este projeto está licenciado sob a **Licença Creative Commons Attribution 4.0 International (CC BY 4.0)**. Isso significa que você é livre para:

- **Compartilhar** — copiar e redistribuir o material em qualquer meio ou formato.
- **Adaptar** — remixar, transformar e construir a partir do material para qualquer fim, inclusive comercialmente.

Desde que sejam cumpridas as seguintes condições:

- **Atribuição** — Você deve dar o devido crédito, fornecer um link para a licença e indicar se foram feitas alterações. Você pode fazê-lo de maneira razoável, mas não de forma que sugira que o licenciante apoia você ou seu uso.

Para mais detalhes sobre os termos da licença, visite: [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/?ref=chooser-v1).

<img src="https://mirrors.creativecommons.org/presskit/icons/cc.large.png" alt="CC Logo" width="150"/><br>

<img src="https://mirrors.creativecommons.org/presskit/icons/by.large.png" alt="CC BY Logo" width="150"/>

[Application 4.0 International](https://creativecommons.org/licenses/by/4.0/?ref=chooser-v1)

# Tags

[Sprint 1](https://github.com/Inteli-College/2024-2A-T01-CC11-G05/releases/tag/SPRINT1)

- Pipeline de Processamento e Base de Dados

- Draft do Artigo

[Sprint 2](https://github.com/Inteli-College/2024-2A-T01-CC11-G05/releases/tag/SPRINT2)

- Artigo com Avaliação Inicial de Modelos de Classificação de Texto

- Implementação de Modelo Baseline (BoW com NB)

- Implementação de Modelo com Rede Neural e Word2Vec pré-treinado


[Sprint 3](https://github.com/Inteli-College/2024-2A-T01-CC11-G05/releases/tag/SPRINT3)

- Artigo com Avaliação de Modelo LSTM ou RNN

- Implementação de Modelo LSTM ou RNN

[Sprint 4](https://github.com/Inteli-College/2024-2A-T01-CC11-G05/releases/tag/SPRINT4)

- Modelo LLM

- Aprimoramento do Frontend

- Atualização do artigo

[Sprint 5](https://github.com/Inteli-College/2024-2A-T01-CC11-G05/releases/tag/SPRINT5)

- Modelo LLAMA 3B

- Finalização do artigo

- Implementação do chatbot
