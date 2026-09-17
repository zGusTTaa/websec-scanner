from sqlalchemy.orm import Session

from web import crud
from websec.core.session import Session as WebsecSession
from websec.models.severity import Severity
from websec.models.target import Target as WebsecTarget
from websec.scanners.headers import HeadersScanner


# Registro de scanners disponíveis
# Quando você criar novos scanners, adiciona aqui
SCANNER_REGISTRY = {
    "headers": HeadersScanner,
}


def run_scan(db: Session, scan_id: int, target_url: str, scanners: list[str] | None) -> int:
    """
    Executa os scanners no alvo e salva os findings no banco.
    Retorna o total de findings salvos.
    """
    # 1. Decide quais scanners rodar
    if scanners is None:
        scanners = list(SCANNER_REGISTRY.keys())

    invalid = [s for s in scanners if s not in SCANNER_REGISTRY]
    if invalid:
        raise ValueError(f"Scanners inválidos: {invalid}")

    # 2. Cria sessão HTTP do motor
    session = WebsecSession(timeout=10)
    target = WebsecTarget(url=target_url)

    total = 0

    try:
        for name in scanners:
            scanner_cls = SCANNER_REGISTRY[name]
            scanner = scanner_cls(session=session)

            try:
                findings = scanner.scan(target)
            except Exception as e:
                # Scanner falhou — loga mas não derruba o scan todo
                print(f"[scanner_service] Erro em {name}: {e}")
                continue

            for finding in findings:
                crud.save_finding(db, scan_id, finding)
                total += 1

        crud.finish_scan(db, scan_id, status="completed")

    except Exception:
        crud.finish_scan(db, scan_id, status="failed")
        raise

    return total