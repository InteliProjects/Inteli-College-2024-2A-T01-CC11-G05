from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.routers import message_routes, conversation_routes, attendant_routes, files_routes
from app.database.config.db import engine
from app.models import database_model
from sqlalchemy.orm import Session
from app.utils.db_utils import load_mock_data
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()


app = FastAPI()

# Inclui os roteadores responsáveis por lidar com diferentes rotas da aplicação
app.include_router(message_routes.router)
app.include_router(conversation_routes.router)
app.include_router(attendant_routes.router)
app.include_router(files_routes.router)

# Obter a URL do frontend
frontend_url = os.getenv("FRONTEND_URL")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],  # Permite solicitações do frontend na porta 3000
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# Monta o diretório estático onde arquivos como HTML, CSS e imagens estão localizados
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def read_root():
    """
    Rota raiz para verificar o funcionamento da API. 
    Retorna uma simples mensagem de "Hello, World".
    """
    return {"Hello": "World"}

@app.on_event("startup")
async def startup_event():
    """
    Evento disparado no início da aplicação.
    Cria as tabelas no banco de dados caso ainda não existam.
    Carrega dados mockados no banco de dados para fins de teste.
    """
    database_model.Base.metadata.create_all(bind=engine)
    
    # Inicia uma sessão de banco de dados e carrega os dados mockados
    with Session(engine) as session:
        load_mock_data(session)

@app.on_event("shutdown")
async def shutdown_event():
    """
    Evento disparado no encerramento da aplicação.
    Aqui podem ser incluídas rotinas para liberar recursos ou fechar conexões de forma segura.
    """
    pass

# Tratamento customizado para erros HTTP 404
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Captura exceções HTTP, como o erro 404 (não encontrado),
    e retorna uma página de erro customizada.
    """
    if exc.status_code == 404:
        return HTMLResponse(content=open("app/static/error.html").read(), status_code=404)
    return HTMLResponse(content=f"{exc.detail}", status_code=exc.status_code)

