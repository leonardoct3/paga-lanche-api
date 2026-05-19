from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database.database import Base, engine
from src.models import runs, user
from src.routers import runs as runs_router
from src.routers import users

API_DESCRIPTION = """
Os Paga Lanche API salva jogadores e suas partidas.

Use esta API para:

- criar e listar usuarios do jogo;
- registrar pontuacao e duracao de cada partida;
- consultar o historico de partidas por usuario.

Endpoints de dados exigem o header `X-API-Key`. No Swagger, clique em
`Authorize` e informe o valor configurado em `API_KEY`.
"""

TAGS_METADATA = [
    {
        "name": "health",
        "description": "Endpoints publicos para verificar se a API esta online.",
    },
    {
        "name": "users",
        "description": "Cadastro e consulta de jogadores.",
    },
    {
        "name": "runs",
        "description": "Registro e consulta das partidas jogadas.",
    },
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Os Paga Lanche API",
    summary="Salvamento de usuarios, pontuacoes e tempo de partida.",
    description=API_DESCRIPTION,
    version="0.1.0",
    contact={
        "name": "Os Paga Lanche",
    },
    openapi_tags=TAGS_METADATA,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(runs_router.router)


@app.get("/", tags=["health"])
def root():
    return {"message": "Os Paga Lanche API"}


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}
