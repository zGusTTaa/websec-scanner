import json
from pathlib import Path

from websec.models.finding import Finding
from websec.models.severity import Severity
from websec.models.target import Target
from websec.scanners.base import BaseScanner

# Headers que revelam tecnologia/versão do servidor
INFO_HEADERS = ["Server", "X-Powered-By", "X-AspNet-Version", "X-Generator"]

# Versões conhecidamente vulneráveis (base local simples)
VULNERABLE_VERSIONS = {
    "apache": ["2.4.49", "2.4.50"],  # CVE-2021-41773 e CVE-2021-42013
    "nginx": ["1.20.0"],             # exemplo didático
    "php": ["5.", "7.0", "7.1"],     # EOL
    "iis": ["6.0", "7.0", "7.5"],    # EOL
}


class ServerInfoScanner(BaseScanner):
    name = "server_info"
    description = "Detecta tecnologia e versões expostas em headers HTTP."

    def scan(self, target: Target) -> list[Finding]:
        findings: list[Finding] = []
        response = self.session.get(target.url)
        if response is None:
            return findings

        for header in INFO_HEADERS:
            value = response.headers.get(header)
            if not value:
                continue

            # Achar a versão vulnerável (se houver)
            vuln_hit = self._check_vulnerable(value)

            if vuln_hit:
                findings.append(
                    Finding(
                        scanner=self.name,
                        severity=Severity.HIGH,
                        url=target.url,
                        description=(
                            f"Versão potencialmente vulnerável exposta em "
                            f"'{header}: {value}'."
                        ),
                        evidence=f"Header {header}: {value} | Padrão: {vuln_hit}",
                        recommendation=(
                            "Atualize o software para a versão mais recente e "
                            "considere remover/omitir headers que revelam versão."
                        ),
                    )
                )
            else:
                findings.append(
                    Finding(
                        scanner=self.name,
                        severity=Severity.LOW,
                        url=target.url,
                        description=(
                            f"Header '{header}' expõe tecnologia do servidor: {value}"
                        ),
                        evidence=f"Header {header}: {value}",
                        recommendation=(
                            f"Considere remover o header '{header}' ou genericar "
                            "seu conteúdo para dificultar fingerprinting."
                        ),
                    )
                )

        return findings

    def _check_vulnerable(self, value: str) -> str | None:
        """Retorna o padrão vulnerável encontrado, ou None."""
        lower = value.lower()
        for tech, versions in VULNERABLE_VERSIONS.items():
            if tech in lower:
                for version in versions:
                    if version in lower:
                        return f"{tech} {version}"
        return None