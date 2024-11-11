# Chatbot

Este diretório contém o código e a configuração para o chatbot.
Aqui está a estrutura revisada com base no seu código:

## Estrutura

- **backend/**: Contém o código e a configuração para o backend do chatbot.
  - **app/**: Código principal do backend.
    - **models/**: Contém os modelos do banco de dados, como `User`, `Conversation`, `Message`, `Feedback`, `AttendantStatus`, `FileSummarization`.
    - **routers/**: Contém os roteadores das rotas da API, como `send_message`, `start_conversation`, `dislike_message`, `upload_image`, etc.
    - **services/**: Lida com a lógica de negócio, como `ChatbotService`, responsável por gerenciar conversas, processar mensagens, áudio, imagens, e feedbacks.
    - **config/**: Arquivos de configuração (conexão de banco de dados, configurações de ambiente, etc.).
    - **database/**: Contém a configuração do banco de dados e as migrações necessárias.
    - **schemas/**: Define os schemas Pydantic usados para validação de dados de entrada/saída, como `ResponseSchema`, `ConversationSchema`, `MessageSchema`, etc.
    - **utils/**: Funções utilitárias que ajudam em tarefas comuns, como manipulação de arquivos e operações de banco de dados.
  - **Dockerfile**: Arquivo Docker para configuração do ambiente de execução do backend.
  - **requirements.txt**: Lista de dependências do backend necessárias para rodar o projeto.
  - **.env**: Variáveis de ambiente para o backend.

- **frontend/**: Contém o código e a configuração para o frontend do chatbot.
  - **public/**: Arquivos públicos do frontend.
  - **src/**: Código-fonte do frontend.
    - **components/**: Componentes do frontend.
    - **pages/**: Páginas do frontend.
    - **services/**: Serviços do frontend.
    - **App.js**: Componente principal do frontend.
    - **index.js**: Ponto de entrada do frontend.
  - **Dockerfile**: Dockerfile para o frontend.
  - **package.json**: Dependências do frontend.
  - **.env**: Variáveis de ambiente para o frontend.

- **docker-compose.yml**: Configuração do Docker Compose para o chatbot.

- **config/**: Arquivos de configuração específicos do chatbot.
  - **app_config.yaml**: Configuração do aplicativo.
  - **logging_config.yaml**: Configuração de logging.

## Configuração e Execução

### Backend

Navegue para o diretório `backend/` e execute:

```bash
docker build -t chatbot-backend .
docker run --env-file .env -p 8000:8000 chatbot-backend
```

### Frontend

Navegue para o diretório `frontend/` e execute:

```bash
docker build -t chatbot-frontend .
docker run -p 3000:3000 chatbot-frontend
```

### Usando Docker Compose

Para executar ambos os serviços simultaneamente navegue para o diretório `src/` e execute:

```bash
docker-compose up
```

## Documentação das APIs

### 1. `/send_message/{conversation_id}`

**Método:** `POST`

**Descrição:** Envia uma mensagem do usuário para o chatbot e retorna uma resposta. Armazena a mensagem e a resposta no banco de dados.

**Corpo da Requisição:**

```json
{
  "user_message": "string"
}
```

**Resposta:**

```json
{
  "status": "success" | "error",
  "message": "Message sent and response received" | "str(e)",
  "data": {
    "response": "string"
  } | None
}
```

**Status Codes:**

- `200 OK`: Mensagem enviada e resposta gerada com sucesso.
- `500 Internal Server Error`: Ocorreu um erro no processamento da mensagem.

---

### 2. `/start_conversation/{user_id}`

**Método:** `POST`

**Descrição:** Inicia uma nova conversa para o usuário especificado e retorna o ID da conversa e as intenções mais comuns.

**Resposta:**

```json
{
  "status": "success" | "error",
  "message": "Conversation started" | "str(e)",
  "data": { 
    "conversation_id": "string",
    "intentions": ["intention1", "intention2"]
  } | None
}
```

**Status Codes:**

- `200 OK`: Conversa iniciada com sucesso.
- `500 Internal Server Error`: Ocorreu um erro ao iniciar a conversa.

---

### 3. `/dislike_message/{conversation_id}/{message_id}`

**Método:** `PATCH`

**Descrição:** Registra um "dislike" em uma mensagem específica de uma conversa.

**Resposta:**

```json
{
  "status": "success" | "error",
  "message": "Dislike recorded" | "str(e)" 
}
```

**Status Codes:**

- `200 OK`: "Dislike" registrado com sucesso.
- `500 Internal Server Error`: Ocorreu um erro ao registrar o "dislike".

---

### 4. `/check_dislikes/{conversation_id}`

**Método:** `GET`

**Descrição:** Verifica se há três "dislikes" consecutivos em uma conversa. Sugere a intervenção de um atendente se necessário.

**Resposta:**

```json
{
  "status": "success" | "error",
  "message": "Dislike check completed" | "str(e)",
  "data": {
    "suggest_attendant": "True" | "False" 
  } | None
}
```

**Status Codes:**

- `200 OK`: Verificação de "dislikes" completada.
- `500 Internal Server Error`: Ocorreu um erro ao verificar os "dislikes".

---

### 5. `/get_conversation/{conversation_id}`

**Método:** `GET`

**Descrição:** Retorna os detalhes de uma conversa específica, incluindo as mensagens trocadas.

**Resposta:**

```json
{
  "status": "success" | "error",
  "message": "Conversation retrieved" | "str(e)",
  "data": {
    "conversation": {
      "id": "string",
      "start_time": "datetime",
      "status": "active" | "ended",
      "messages": [
        {
          "user_message": "string",
          "response_message": "string",
          "disliked": "boolean"
        }
      ]
    }
  } | None
}
```

**Status Codes:**

- `200 OK`: Conversa recuperada com sucesso.
- `404 Not Found`: Conversa não encontrada.
- `500 Internal Server Error`: Ocorreu um erro ao recuperar a conversa.

---

### 6. `/end_conversation/{conversation_id}`

**Método:** `POST`

**Descrição:** Encerra uma conversa ativa.

**Resposta:**

```json
{
  "status": "success" | "error",
  "message": "Conversation ended" | "str(e)"
}
```

**Status Codes:**

- `200 OK`: Conversa encerrada com sucesso.
- `500 Internal Server Error`: Ocorreu um erro ao encerrar a conversa.

---

### 7. `/user_feedback`

**Método:** `POST`

**Descrição:** Envia o feedback do usuário sobre uma conversa.

**Corpo da Requisição:**

```json
{
  "conversation_id": "string",
  "rating": "int range(1,5)",
  "comments": "string"
}
```

**Resposta:**

```json
{
  "status": "success" | "error",
  "message": "Feedback received" | "str(e)"
}
```

**Status Codes:**

- `200 OK`: Feedback recebido com sucesso.
- `500 Internal Server Error`: Ocorreu um erro ao processar o feedback.

---

### 8. `/attendant_status`

**Método:** `GET`

**Descrição:** Retorna o status do atendente (disponível ou não).

**Resposta:**

```json
{
  "status": "success" | "error",
  "message": "Attendant status retrieved" | "str(e)",
  "data": {
    "status": "Available" | "Unavailable"
  } | None
}
```

**Status Codes:**

- `200 OK`: Status do atendente retornado com sucesso.
- `500 Internal Server Error`: Ocorreu um erro ao verificar o status do atendente.

---

### 9. `/upload_image/{conversation_id}`

**Método:** `POST`

**Descrição:** Faz o upload de uma imagem ou PDF, processa e resume o conteúdo.

**Parâmetros de URL:**

- `conversation_id` (string): ID da conversa.

**Corpo da Requisição:** Arquivo (imagem ou PDF)

**Resposta:**

```json
{
  "status": "success" | "error",
  "message": "Image processed successfully" | "str(e)",
  "data": {
    "response_message": "string"
  } | None
}
```

**Status Codes:**

- `200 OK`: Imagem processada com sucesso.
- `400 Bad Request`: Tipo de arquivo não suportado.
- `500 Internal Server Error`: Ocorreu um erro ao processar a imagem.

---

### 10. `/upload_audio/{conversation_id}`

**Método:** `POST`

**Descrição:** Faz o upload de um arquivo de áudio, processa e resume o conteúdo.

**Parâmetros de URL:**

- `conversation_id` (string): ID da conversa.

**Corpo da Requisição:** Arquivo de áudio

**Resposta:**

```json
{
  "status": "success" | "error",
  "message": "Audio processed successfully" | "str(e)",
  "data": {
    "response_message": "string"
  } | None
}
```

**Status Codes:**

- `200 OK`: Áudio processado com sucesso.
- `500 Internal Server Error`: Ocorreu um erro ao processar o áudio.

---

## Documentação do Banco de Dados

### Tabelas e Esquemas


#### 1. `users`

- **Descrição:** Armazena informações sobre os usuários.
- **Colunas:**
  - `id` (String, Primary Key): ID único do usuário.
  - `name` (String): Nome do usuário.
  

#### 2. `conversations`

- **Descrição:** Armazena informações sobre as conversas.
- **Colunas:**
  - `id` (String, Primary Key): ID único da conversa.
  - `start_time` (DateTime): Data e hora de início da conversa.
  - `status` (String): Status da conversa (por exemplo, "active", "ended").
  - `intentions` (ARRAY(Text)): Intenções comuns da conversa.
  - `user_id` (String, Foreign Key): ID do usuário associado.
  - `end_time` (DateTime): Data e hora do fim da conversa.

#### 3. `messages`

- **Descrição:** Armazena as mensagens trocadas dentro de uma conversa.
- **Colunas:**
  - `id` (Integer, Primary Key): ID único da mensagem.
  - `conversation_id` (String, Foreign Key): ID da conversa à qual a mensagem pertence.
  - `user_message` (String): Mensagem enviada pelo usuário.
  - `response_message` (String): Resposta gerada pelo chatbot.
  - `timestamp` (DateTime): Data e hora da mensagem.
  - `disliked` (Boolean): Indica se a mensagem foi "desliked".

#### 4. `feedbacks`

- **Descrição:** Armazena o feedback do usuário sobre as conversas.
- **Colunas:**
  - `id` (Integer, Primary Key): ID único do feedback.
  - `conversation_id` (String, Foreign Key): ID da conversa associada.
  - `rating` (Integer): Avaliação fornecida pelo usuário.
  - `comments` (String): Comentários do usuário.
  - `timestamp` (DateTime): Data e hora do feedback.

#### 5. `attendant_status`

- **Descrição:** Armazena o status do atendente.
- **Colunas:**
  - `id` (Integer, Primary Key): ID único do status.
  - `name` (String): Nome do atendente.
  - `status` (Boolean): Status atual do atendente (disponível ou não).
  - `updated_at` (DateTime): Data e hora do atendente disponível.

#### 6. `file_summarizations`

- **Descrição:** Armazena sumarizações de arquivos de áudio ou imagem enviados pelo usuário.
- **Colunas:**
  - `id` (String, Primary Key): ID único da sumarização.
  - `conversation_id` (String, Foreign Key): ID da conversa associada.
  - `file_type` (Enum): Tipo de arquivo (áudio ou imagem).
  - `summarization` (Text): Texto da sumarização.
  - `timestamp` (DateTime): Data e hora da sumarização.

