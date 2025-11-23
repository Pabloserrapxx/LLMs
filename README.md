### 1. 🤖 Chatbot RAG Local com Docker e Ollama
> **Stack:** Python, LangChain, ChromaDB, FastAPI, Docker, Vanilla JS.

Este projeto é uma implementação Full Stack do padrão **RAG (Retrieval-Augmented Generation)**, projetada para rodar inteiramente em ambiente local, garantindo privacidade e controle total sobre os dados.
* **Arquitetura de Microsserviços:** O sistema é orquestrado via Docker Compose, separando o frontend, a API de backend e o serviço de inferência de LLM (Ollama) em containers isolados para fácil implantação.
* **Motor de RAG:** Utiliza **LangChain** para gerenciar o fluxo de ingestão de documentos e **ChromaDB** para a indexação vetorial, permitindo que o modelo `TinyLlama` responda perguntas com base em um contexto privado injetado dinamicamente.
* **Interface Reativa:** Conta com um frontend moderno desenvolvido em JavaScript puro (Vanilla JS) que se comunica de forma assíncrona com a API FastAPI, oferecendo feedback visual de carregamento e histórico de chat.

