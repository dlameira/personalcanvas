#!/usr/bin/env python3
"""
Servidor local para o personalcanvas.
Serve arquivos estáticos + aceita POST /save-memory para escrever CLAUDE.md.
"""
import http.server, json, os, urllib.parse
from pathlib import Path

PORT = 3000
ROOT = Path(__file__).parent

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(ROOT), **kw)

    def do_POST(self):
        if self.path == '/save-memory':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body)
                content = data.get('content', '')
                (ROOT / 'CLAUDE.md').write_text(content, encoding='utf-8')
                self._respond(200, {'ok': True})
            except Exception as e:
                self._respond(500, {'error': str(e)})
        else:
            self._respond(404, {'error': 'not found'})

    def _respond(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(body))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, fmt, *args):
        pass  # silencia logs

if __name__ == '__main__':
    import socketserver
    with socketserver.TCPServer(('', PORT), Handler) as httpd:
        print(f'personalcanvas → http://localhost:{PORT}')
        httpd.serve_forever()
