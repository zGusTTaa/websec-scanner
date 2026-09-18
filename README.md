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
