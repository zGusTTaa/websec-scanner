from fastapi import FastAPI

from web.database import Base, engine
from web.routes import targets

# Cria as tabelas automaticamente se ainda não existirem
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="WebSec Scanner API",
    description="API para gerenciar alvos, scans e vulnerabilidades.",
    version="0.1.0",
)

# Registra as rotas
app.include_router(targets.router)


@app.get("/", tags=["Root"])
def root():
    """Endpoint raiz — útil para checar se o servidor está de pé."""
    return {
        "app": "WebSec Scanner API",
        "version": "0.1.0",
        "docs": "/docs",
    }