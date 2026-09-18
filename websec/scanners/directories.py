from concurrent.futures import ThreadPoolExecutor, as_completed

from websec.models.finding import Finding
from websec.models.severity import Severity
from websec.models.target import Target
from websec.scanners.base import BaseScanner


COMMON_PATHS = {
    "/admin": Severity.MEDIUM,
    "/admin/": Severity.MEDIUM,
    "/login": Severity.LOW,
    "/.env": Severity.CRITICAL,
    "/.git/config": Severity.CRITICAL,
    "/.git/HEAD": Severity.CRITICAL,
    "/backup.zip": Severity.HIGH,
    "/backup.sql": Severity.CRITICAL,
    "/backup.tar.gz": Severity.HIGH,
    "/db.sql": Severity.CRITICAL,
    "/database.sql": Severity.CRITICAL,
    "/config.php": Severity.HIGH,
    "/wp-config.php": Severity.HIGH,
    "/phpinfo.php": Severity.HIGH,
    "/server-status": Severity.MEDIUM,
    "/.htaccess": Severity.MEDIUM,
    "/robots.txt": Severity.INFO,
    "/sitemap.xml": Severity.INFO,
    "/api": Severity.INFO,
    "/swagger": Severity.INFO,
    "/docs": Severity.INFO,
}

MAX_WORKERS = 10          # requisições simultâneas
PER_REQUEST_TIMEOUT = 5   # segundos por requisição


class DirectoriesScanner(BaseScanner):
    name = "directories"
    description = "Procura diretórios e arquivos sensíveis expostos."

    def scan(self, target: Target) -> list[Finding]:
        base = target.url.rstrip("/")
        findings: list[Finding] = []

        def check_path(path: str, severity: Severity) -> Finding | None:
            url = f"{base}{path}"
            response = self.session.get(url, timeout=PER_REQUEST_TIMEOUT)
            if response is None:
                return None

            if response.status_code == 200:
                return Finding(
                    scanner=self.name,
                    severity=severity,
                    url=url,
                    description=f"Recurso acessível publicamente: {path}",
                    evidence=f"HTTP 200 — {len(response.content)} bytes",
                    recommendation=f"Restrinja o acesso a '{path}' ou remova o arquivo do servidor.",
                )
            if response.status_code == 403:
                return Finding(
                    scanner=self.name,
                    severity=Severity.INFO,
                    url=url,
                    description=f"Recurso existe mas está bloqueado: {path}",
                    evidence="HTTP 403",
                    recommendation=f"'{path}' existe. Considere removê-lo se não for necessário.",
                )
            return None

        # Executa todas as requisições em paralelo
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {
                executor.submit(check_path, path, severity): path
                for path, severity in COMMON_PATHS.items()
            }
            for future in as_completed(futures):
                try:
                    finding = future.result()
                    if finding:
                        findings.append(finding)
                except Exception as e:
                    path = futures[future]
                    print(f"[directories] Erro em {path}: {e}")

        return findings