# Projeto RAG Local com Ollama

Este projeto implementa um sistema de RAG (Retrieval-Augmented Generation) local utilizando Docker, Ollama e Python.

## Pré-requisitos

- [Docker](https://www.docker.com/products/docker-desktop/) instalado e rodando.

## Como Rodar

1.  Abra um terminal na raiz do projeto (`.../LLMs`).
2.  Execute o comando para construir e iniciar os containers:

    ```bash
    docker-compose up --build
    ```

3.  Aguarde a inicialização.
    - Na primeira execução, o serviço pode demorar alguns minutos para baixar o modelo `tinyllama` automaticamente.
    - Fique atento aos logs no terminal. Quando vir mensagens indicando que o servidor Uvicorn iniciou (`Application startup complete`), o sistema está pronto.

4.  Acesse a interface web no seu navegador:

    [http://localhost:8000](http://localhost:8000)

## Estrutura

- **Frontend**: HTML/JS/CSS puro, servido pelo FastAPI.
- **Backend**: FastAPI (`backend/main.py`) que gerencia as requisições.
- **RAG Service**: Lógica de ingestão e consulta (`backend/rag_service.py`).
- **Ollama**: Serviço de LLM rodando em um container separado.

## Notas

- O texto base para o RAG está hardcoded em `backend/rag_service.py` para fins de demonstração.
- O modelo utilizado é o `tinyllama`.
