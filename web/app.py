from fastapi import FastAPI

from web.database import Base, engine
from web.routes import findings, scans, targets

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="WebSec Scanner API",
    description="API para gerenciar alvos, scans e vulnerabilidades.",
    version="0.1.0",
)

app.include_router(targets.router)
app.include_router(scans.router)
app.include_router(findings.router)


@app.get("/", tags=["Root"])
def root():
    return {
        "app": "WebSec Scanner API",
        "version": "0.1.0",
        "docs": "/docs",
    }