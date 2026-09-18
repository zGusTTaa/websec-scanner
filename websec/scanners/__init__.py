"""Scanners de vulnerabilidade disponíveis."""

from websec.scanners.headers import HeadersScanner
from websec.scanners.server_info import ServerInfoScanner

SCANNER_REGISTRY = {
    "headers": HeadersScanner,
    "server_info": ServerInfoScanner,
}

__all__ = ["SCANNER_REGISTRY"]