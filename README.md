# 🔒 WebSec Scanner

Ferramenta de análise de vulnerabilidades web com **dashboard visual** e **API REST documentada**. Detecta problemas comuns de segurança em aplicações HTTP.

> ⚠️ **Uso ético apenas.** Esta ferramenta deve ser usada exclusivamente em alvos que você possui ou tem autorização explícita para testar. Uso não autorizado é crime.

---

## ✨ Funcionalidades

- **Scanner de headers de segurança** — detecta CSP, HSTS, X-Frame-Options ausentes
- **Análise de informações do servidor** — identifica tecnologias e versões expostas
- **Descoberta de diretórios sensíveis** — procura por `/admin`, `/.env`, `/backup.zip`, etc.
- **Dashboard web** — visualização de alvos, scans e findings com filtros
- **API REST** — todos os recursos acessíveis via HTTP (documentação em `/docs`)
- **Scan em background** — não bloqueia a interface, progresso acompanhado por polling

---

## 🛠 Stack

| Camada | Tecnologia |
|---|---|
| Motor do scanner | Python 3.12 + `requests` + `BeautifulSoup` |
| API | FastAPI + Uvicorn |
| Banco | SQLite + SQLAlchemy 2.0 |
| Front-end | HTML + CSS + JavaScript puro |
| Templates | Jinja2 |
| CLI | `argparse` + `rich` |

---

## 🏗 Arquitetura



**O motor (`websec/`) é independente da API.** Ele pode ser usado via CLI (`python -m websec --url ...`) ou consumido pela aplicação web (`web/`). Essa separação permite evoluir os dois lados sem quebrar nada.

---

## 🚀 Como rodar

### Pré-requisitos
- Python 3.12+
- pip
- Git

### Instalação

```bash
# Clone o repositório
git clone https://github.com/zGusTTaa/websec-scanner.git
cd websec-scanner

# Crie o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .\.venv\Scripts\Activate.ps1  # Windows

# Instale as dependências
pip install -r requirements.txt

# Copie o template de variáveis de ambiente
cp .env.example .env
