# Implementação de Chatbot RAG Full Stack (Frontend + Backend)

## Objetivo
Transformar o script CLI existente em uma aplicação web completa com arquitetura cliente-servidor, mantendo a infraestrutura Docker/Ollama.

## Mudanças Propostas

### 1. Estrutura de Diretórios
Organizar o projeto para separar responsabilidades:
```
/app
  /backend
    main.py (API FastAPI)
    rag_service.py (Lógica de RAG e Setup)
  /frontend
    index.html
    style.css
    script.js
  Dockerfile
  docker-compose.yml
  requirements.txt
```

### 2. Backend (FastAPI)
- **Framework**: FastAPI (rápido, moderno, assíncrono).
- **Endpoints**:
  - `GET /`: Serve o frontend.
  - `POST /api/chat`: Recebe a mensagem do usuário, processa via RAG, retorna a resposta.
  - `GET /health`: Verifica status do Ollama.
- **Startup**: Manter a lógica de verificação/download do modelo "tinyllama" no evento de startup da API.

### 3. Frontend (HTML/CSS/JS)
- **Design**: Interface moderna estilo "Chat", com tema escuro, animações suaves e responsividade.
- **Tecnologia**: Vanilla JS + CSS (sem necessidade de build complexo de React/Vue para este escopo, mantendo simplicidade no Docker).
- **Funcionalidades**:
  - Histórico de chat.
  - Indicador de "Digitando..." (Loading).
  - Auto-scroll.

### 4. Infraestrutura (Docker)
- **requirements.txt**: Adicionar `fastapi`, `uvicorn`.
- **Dockerfile**: Ajustar para instalar novas deps e rodar com `uvicorn`.
- **docker-compose.yml**: Expor porta 8000 (padrão FastAPI/Uvicorn).

## Plano de Execução
1. Atualizar `requirements.txt`.
2. Refatorar lógica RAG para `backend/rag_service.py`.
3. Criar servidor API em `backend/main.py`.
4. Criar interface em `frontend/`.
5. Atualizar configurações Docker.
