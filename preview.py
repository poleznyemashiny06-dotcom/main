#!/usr/bin/env python3
"""One-click local preview for the static site."""

from __future__ import annotations

import argparse
import http.server
import socket
import socketserver
import threading
import time
import webbrowser
from pathlib import Path


def find_free_port(preferred: int) -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        if sock.connect_ex(("127.0.0.1", preferred)) != 0:
            return preferred

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def run_server(port: int, directory: Path, no_browser: bool) -> None:
    handler = http.server.SimpleHTTPRequestHandler
    socketserver.TCPServer.allow_reuse_address = True

    with socketserver.TCPServer(("127.0.0.1", port), handler) as httpd:
        url = f"http://127.0.0.1:{port}/index.html"
        print("=" * 60)
        print("✅ Предпросмотр готов")
        print(f"Откройте в браузере: {url}")
        print("Чтобы остановить сервер: Ctrl+C")
        print("=" * 60)

        if not no_browser:
            threading.Thread(target=lambda: (time.sleep(0.4), webbrowser.open(url)), daemon=True).start()

        httpd.serve_forever()


def main() -> None:
    parser = argparse.ArgumentParser(description="Запуск визуального предпросмотра сайта")
    parser.add_argument("--port", type=int, default=8000, help="Порт предпросмотра (по умолчанию: 8000)")
    parser.add_argument("--no-browser", action="store_true", help="Не открывать браузер автоматически")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent
    port = find_free_port(args.port)

    # Serve files from repo root so index.html and styles.css resolve directly.
    import os

    os.chdir(project_root)
    run_server(port=port, directory=project_root, no_browser=args.no_browser)


if __name__ == "__main__":
    main()
