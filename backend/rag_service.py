import os
import time
import requests
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain.docstore.document import Document

# Configurações
OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
MODEL_NAME = "tinyllama"

class RAGService:
    def __init__(self):
        self.vectorstore = None
        self.llm = None

    def check_and_download_model(self):
        """
        Verifica se o modelo existe no Ollama e baixa se necessário.
        """
        print(f"--- RAG Service: Verificação do Modelo ({MODEL_NAME}) ---")
        print(f"Conectando ao Ollama em: {OLLAMA_URL}")
        
        # Loop de espera
        max_retries = 30
        for i in range(max_retries):
            try:
                requests.get(OLLAMA_URL)
                print("Conexão com Ollama estabelecida.")
                break
            except requests.exceptions.ConnectionError:
                print(f"Aguardando serviço Ollama iniciar... ({i+1}/{max_retries})")
                time.sleep(2)
        else:
            raise Exception("Não foi possível conectar ao serviço Ollama.")

        # Verifica e baixa modelo
        try:
            response = requests.get(f"{OLLAMA_URL}/api/tags")
            if response.status_code == 200:
                models_info = response.json().get('models', [])
                model_exists = any(MODEL_NAME in m['name'] for m in models_info)
                
                if not model_exists:
                    print(f"Modelo '{MODEL_NAME}' não encontrado. Baixando...")
                    requests.post(f"{OLLAMA_URL}/api/pull", json={"name": MODEL_NAME}, stream=True)
                    print(f"Modelo '{MODEL_NAME}' baixado com sucesso!")
                else:
                    print(f"Modelo '{MODEL_NAME}' já disponível.")
            else:
                print(f"Erro ao listar modelos: {response.status_code}")
        except Exception as e:
            print(f"Erro crítico na verificação do modelo: {e}")
            raise

    def initialize_rag(self):
        """
        Inicializa o pipeline RAG (Embeddings, Vectorstore, LLM)
        """
        print("--- RAG Service: Inicializando Pipeline ---")
        
        # Texto base fixo para este exemplo
        texto_fonte = "Pablo é um especialista em MLOps que está testando arquiteturas de containers Docker."
        
        print("Gerando embeddings e indexando...")
        embeddings = OllamaEmbeddings(model=MODEL_NAME, base_url=OLLAMA_URL)
        
        # Cria banco vetorial em memória
        self.vectorstore = Chroma.from_texts(
            texts=[texto_fonte],
            embedding=embeddings
        )
        
        self.llm = ChatOllama(model=MODEL_NAME, base_url=OLLAMA_URL)
        print("Pipeline RAG pronto!")

    def query(self, question: str):
        """
        Executa uma consulta no sistema RAG
        """
        if not self.vectorstore or not self.llm:
            return "Erro: Sistema RAG não inicializado."

        print(f"Processando pergunta: {question}")
        
        # Recupera contexto
        retriever = self.vectorstore.as_retriever()
        docs = retriever.get_relevant_documents(question)
        contexto = docs[0].page_content if docs else ""
        
        # Gera resposta
        prompt_final = f"Use o seguinte contexto para responder à pergunta.\nContexto: {contexto}\nPergunta: {question}\nResposta:"
        resposta = self.llm.invoke(prompt_final)
        
        return {
            "answer": resposta.content,
            "context": contexto
        }

# Instância global
rag_service = RAGService()
