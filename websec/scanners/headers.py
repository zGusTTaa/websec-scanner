from websec.models.finding import Finding
from websec.models.severity import Severity
from websec.models.target import Target
from websec.scanners.base import BaseScanner


SECURITY_HEADERS = {
    "Content-Security-Policy": (
        Severity.HIGH,
        "Sem CSP, a aplicação fica vulnerável a XSS e injeção de conteúdo.",
        "Defina uma política de Content-Security-Policy restritiva.",
    ),
    "X-Frame-Options": (
        Severity.MEDIUM,
        "Sem X-Frame-Options, a página pode ser embutida em iframes (clickjacking).",
        "Defina X-Frame-Options: DENY ou SAMEORIGIN.",
    ),
    "Strict-Transport-Security": (
        Severity.MEDIUM,
        "Sem HSTS, conexões podem ser rebaixadas para HTTP.",
        "Adicione Strict-Transport-Security com max-age adequado.",
    ),
    "X-Content-Type-Options": (
        Severity.LOW,
        "Sem nosniff, o navegador pode interpretar arquivos com MIME errado.",
        "Adicione X-Content-Type-Options: nosniff.",
    ),
    "Referrer-Policy": (
        Severity.LOW,
        "Sem Referrer-Policy, URLs internas podem vazar para terceiros.",
        "Defina Referrer-Policy: strict-origin-when-cross-origin.",
    ),
}


class HeadersScanner(BaseScanner):
    name = "headers"
    description = "Verifica headers de segurança HTTP ausentes."

    def scan(self, target: Target) -> list[Finding]:
        findings: list[Finding] = []
        response = self.session.get(target.url)
        if response is None:
            return findings

        for header, (severity, description, recommendation) in SECURITY_HEADERS.items():
            if header not in response.headers:
                findings.append(
                    Finding(
                        scanner=self.name,
                        severity=severity,
                        url=target.url,
                        description=f"Header ausente: {header}. {description}",
                        evidence=f"Headers recebidos: {list(response.headers.keys())}",
                        recommendation=recommendation,
                    )
                )
        return findings