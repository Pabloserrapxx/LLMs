import os
import time
import requests
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain.docstore.document import Document

# Configurações
# OLLAMA_BASE_URL é definido no docker-compose.yml
OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
MODEL_NAME = "tinyllama"

def check_and_download_model():
    """
    Passo A: Verificação e Download Automático do Modelo
    """
    print(f"--- Passo A: Verificação do Modelo ({MODEL_NAME}) ---")
    print(f"Conectando ao Ollama em: {OLLAMA_URL}")
    
    # Loop de espera para garantir que o container do Ollama esteja pronto
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
        raise Exception("Não foi possível conectar ao serviço Ollama após várias tentativas.")

    # Verifica se o modelo já existe
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags")
        if response.status_code == 200:
            models_info = response.json().get('models', [])
            # Verifica se 'tinyllama' está em algum dos nomes de modelo retornados
            model_exists = any(MODEL_NAME in m['name'] for m in models_info)
            
            if not model_exists:
                print(f"Modelo '{MODEL_NAME}' não encontrado. Baixando modelo, aguarde... (Isso pode demorar um pouco)")
                # POST para baixar o modelo
                pull_response = requests.post(f"{OLLAMA_URL}/api/pull", json={"name": MODEL_NAME}, stream=True)
                
                # Apenas para mostrar progresso simples
                for line in pull_response.iter_lines():
                    if line:
                        # Decodifica a linha para string, se necessário processar o JSON de progresso
                        pass 
                print(f"Modelo '{MODEL_NAME}' baixado com sucesso!")
            else:
                print(f"Modelo '{MODEL_NAME}' já está disponível no servidor.")
        else:
            print(f"Erro ao listar modelos: {response.status_code}")
            
    except Exception as e:
        print(f"Erro crítico na verificação do modelo: {e}")
        raise

def run_rag_pipeline():
    """
    Executa o pipeline RAG: Ingestão -> Consulta -> Avaliação
    """
    
    # Passo B: Ingestão de Dados (RAG)
    print("\n--- Passo B: Ingestão de Dados ---")
    texto_fonte = "Pablo é um especialista em MLOps que está testando arquiteturas de containers Docker."
    print(f"Texto base: '{texto_fonte}'")
    
    print("Gerando embeddings e indexando no ChromaDB...")
    # Inicializa embeddings usando o modelo no Ollama
    embeddings = OllamaEmbeddings(model=MODEL_NAME, base_url=OLLAMA_URL)
    
    # Cria o banco vetorial em memória (para teste rápido)
    # Se quisesse persistir, adicionaria o parâmetro persist_directory="./chroma_db"
    vectorstore = Chroma.from_texts(
        texts=[texto_fonte],
        embedding=embeddings
    )
    
    # Passo C: Consulta (Query)
    print("\n--- Passo C: Consulta ---")
    pergunta = "O que o Pablo está testando?"
    print(f"Pergunta: '{pergunta}'")
    
    # Recupera documentos relevantes
    retriever = vectorstore.as_retriever()
    docs = retriever.get_relevant_documents(pergunta)
    
    if docs:
        contexto = docs[0].page_content
        print(f"Contexto recuperado do Chroma: '{contexto}'")
    else:
        contexto = ""
        print("Nenhum contexto relevante encontrado.")
    
    # Inicializa o Chat Model
    llm = ChatOllama(model=MODEL_NAME, base_url=OLLAMA_URL)
    
    # Gera a resposta usando o contexto
    prompt_final = f"Use o seguinte contexto para responder à pergunta.\nContexto: {contexto}\nPergunta: {pergunta}\nResposta:"
    resposta = llm.invoke(prompt_final)
    print(f"Resposta do Modelo: {resposta.content}")
    
    # Passo D: Auto-Avaliação (LLM-as-a-Judge)
    print("\n--- Passo D: Auto-Avaliação ---")
    prompt_avaliacao = f"Dê uma nota de 0 a 10 para a resposta anterior baseada na clareza. Resposta avaliada: '{resposta.content}'. Retorne apenas a nota numérica."
    avaliacao = llm.invoke(prompt_avaliacao)
    print(f"Nota de Auto-Avaliação: {avaliacao.content}")

if __name__ == "__main__":
    # Aguarda um pouco para garantir que o container do Ollama subiu completamente o servidor HTTP
    time.sleep(5)
    check_and_download_model()
    run_rag_pipeline()
