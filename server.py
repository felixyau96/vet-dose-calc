#!/usr/bin/env python3
"""Static file server for the veterinary dose calculator."""
import http.server
import socketserver
import os
import sys

PORT = int(os.environ.get("DOSE_CALC_PORT", "8787"))
HOST = "0.0.0.0"
ROOT = os.path.dirname(os.path.abspath(__file__))


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()


def main():
    os.chdir(ROOT)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((HOST, PORT), Handler) as httpd:
        print(f"Serving {ROOT} at http://{HOST}:{PORT}/", flush=True)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.", flush=True)
            sys.exit(0)


if __name__ == "__main__":
    main()
