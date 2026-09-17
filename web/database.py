from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# SQLite local — o arquivo websec.db é criado na raiz do projeto
DATABASE_URL = "sqlite:///./websec.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # obrigatório para SQLite + FastAPI
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base para todos os modelos SQLAlchemy."""
    pass


def get_db():
    """Dependency do FastAPI que fornece uma sessão do banco."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()