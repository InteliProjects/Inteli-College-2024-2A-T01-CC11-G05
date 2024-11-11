# Implementação de Desafio

Conforme solicitado, um adicional foi implementado no projeto, e dentre as opções previstas. A escolhida foi:

- Realizar processamento de imagens de forma local (dentro de API própria) (documentação + código)

## Ferramentas Utilizadas

Duas AIs locais foram utilizadas nos processos de Extração de Dados da imagem e Sumarização de Texto:

- Extração de Dados: O pytesseract foi utilizado como biblioteca de reconhecimento de texto em imagens. O tesseract é um OCR (Optical Character Recognition) e o pytesseract é sua implementação em Python, linguagem de programação do backend

- Sumarização de Texto: O BART (Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension) desenvolvido pelo META, recebe textos como input e cria uma sumarização baseada no contexto, ele utiliza os próprios dados da Meta para treinamento.

## Estrutura

Dentro do **backend/** do projeto, a API que realiza o envio da mensagem e devolve a resposta fornecida pelo chatbot é `/upload_image/{conversation_id}`. Os casos de uso mostram

## Execução

![Frase Albert Einstein](<imgs_desafio/Frase Albert Einstein.jpg>)

<div style="text-align: center;">
Figura 1: Imagem teste com texto de reflexão de Albert Einstein
</div>

![alt text](<imgs_desafio/Teste Desafio.png>)
<div style="text-align: center;">
Figura 2: Texto extraído pelo pytesseract e texto sumarizado pelo BART
</div>

## Limitações

O modelo pytesseract possui uma boa acurácia em extrair texto de imagens, mesmo utilizando a biblioteca em português, o que se espera que seja menos eficaz comparado com a língua de treinamento original.

Porém, o BART foi treinado primariamente com os dados do Meta, e mesmo que sejam diversificados, a linguagem de atuação do modelo é inglês. Conforme o exemplo, o modelo possui outputs convolutos e desordenados para textos em inglês, repetindo até mesmo partes do texto sem sumarizar. Um ponto a melhorar seria ou o fine-tuning deste modelo para linguagem PT-BR, ou a implementação de outro modelo com melhor trabalho na linguagem PT-BR.

Por último, vale ressaltar que as imagens enviadas serão em boa parte em japonês, linguagem que o parceiro opera em conjunto com português. Isso acarretaria na necessidade de modelos de maior complexidade de entendimento de linguagens, o que pode facilmente torna-se infactível para rodar localmente, dependendo das especificações técnicas.