import argparse
import sys

from rich.console import Console
from rich.table import Table

from websec.core.session import Session
from websec.models.target import Target
from websec.scanners.headers import HeadersScanner

console = Console()


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="websec",
        description="WebSec Scanner — análise de vulnerabilidades web (uso ético apenas).",
    )
    parser.add_argument("--url", required=True, help="URL alvo do scan")
    parser.add_argument("--timeout", type=int, default=10, help="Timeout em segundos")
    args = parser.parse_args()

    console.print(f"[bold cyan]→ Escaneando:[/] {args.url}")

    session = Session(timeout=args.timeout)
    scanner = HeadersScanner(session=session)
    target = Target(url=args.url)

    findings = scanner.scan(target)

    if not findings:
        console.print("[bold green]✅ Nenhuma vulnerabilidade encontrada.[/]")
        sys.exit(0)

    table = Table(title=f"Findings — {args.url}")
    table.add_column("Severidade", style="bold")
    table.add_column("Descrição")

    for f in findings:
        table.add_row(f"[{f.severity.color}]{f.severity.label}[/]", f.description)

    console.print(table)


if __name__ == "__main__":
    main()