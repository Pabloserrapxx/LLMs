from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from rag_service import rag_service
import os

app = FastAPI()

# Modelo de dados para requisição
class ChatRequest(BaseModel):
    message: str

@app.on_event("startup")
async def startup_event():
    """
    Executa verificação do modelo e inicialização do RAG ao iniciar a API
    """
    try:
        rag_service.check_and_download_model()
        rag_service.initialize_rag()
    except Exception as e:
        print(f"Erro fatal na inicialização: {e}")

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "RAG Chatbot"}

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        response = rag_service.query(request.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Monta o frontend estático na raiz
# Nota: '../frontend' assume que estamos rodando de dentro de /app/backend ou ajustaremos o workdir
# No Docker, workdir é /app, então caminhos relativos precisam de cuidado.
# Vamos assumir que rodaremos o uvicorn de /app, então 'frontend' está em './frontend'
app.mount("/", StaticFiles(directory="../frontend", html=True), name="static")
