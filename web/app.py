from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from web.database import Base, engine
from web.routes import findings, pages, scans, targets

Base.metadata.create_all(bind=engine)

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="WebSec Scanner API",
    description="API para gerenciar alvos, scans e vulnerabilidades.",
    version="0.1.0",
)

# Estáticos (CSS, JS, imagens)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Rotas da API
app.include_router(targets.router)
app.include_router(scans.router)
app.include_router(findings.router)

# Rotas das páginas HTML
app.include_router(pages.router)


@app.get("/api/health", tags=["Root"])
def health():
    return {"status": "ok", "version": "0.1.0"}