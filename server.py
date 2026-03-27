#!/usr/bin/env python3
"""
Servidor local para o personalcanvas.
Serve arquivos estáticos + API para persistência no GitHub.
"""
import http.server, json, os, subprocess
from pathlib import Path

PORT = 3000
ROOT = Path(__file__).parent

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(ROOT), **kw)

    def do_GET(self):
        if self.path.startswith('/api/state'):
            self._serve_state()
        elif self.path.startswith('/api/git-status'):
            self._serve_git_status()
        else:
            super().do_GET()

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)
        try:
            data = json.loads(body)
        except Exception:
            self._respond(400, {'error': 'invalid json'}); return

        if self.path == '/api/save-state':
            self._save_state(data)
        elif self.path == '/save-memory':
            self._save_memory(data)
        else:
            self._respond(404, {'error': 'not found'})

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    # ── handlers ─────────────────────────────────────────────────

    def _serve_state(self):
        path = ROOT / 'state.json'
        if not path.exists():
            self._respond(404, {'error': 'state.json not found'}); return
        content = path.read_bytes()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(content))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(content)

    def _serve_git_status(self):
        try:
            r = subprocess.run(['git', 'status', '--porcelain'], cwd=str(ROOT),
                               capture_output=True, text=True)
            dirty = bool(r.stdout.strip())
            log = subprocess.run(['git', 'log', '--oneline', '-1'], cwd=str(ROOT),
                                 capture_output=True, text=True).stdout.strip()
            self._respond(200, {'dirty': dirty, 'last_commit': log})
        except Exception as e:
            self._respond(500, {'error': str(e)})

    def _save_state(self, data):
        state   = data.get('state')
        message = data.get('message', 'update canvas state')
        if state is None:
            self._respond(400, {'error': 'missing state'}); return
        try:
            path = ROOT / 'state.json'
            path.write_text(json.dumps(state, ensure_ascii=False, indent=2),
                            encoding='utf-8')
            subprocess.run(['git', 'add', 'state.json'], cwd=str(ROOT), check=True)
            result = subprocess.run(['git', 'commit', '-m', message],
                                    cwd=str(ROOT), capture_output=True, text=True)
            if 'nothing to commit' in result.stdout + result.stderr:
                self._respond(200, {'ok': True, 'committed': False, 'note': 'nothing changed'})
                return
            subprocess.run(['git', 'push'], cwd=str(ROOT), check=True)
            self._respond(200, {'ok': True, 'committed': True, 'message': message})
        except subprocess.CalledProcessError as e:
            self._respond(200, {'ok': True, 'committed': False, 'error': e.stderr})
        except Exception as e:
            self._respond(500, {'error': str(e)})

    def _save_memory(self, data):
        try:
            content = data.get('content', '')
            (ROOT / 'CLAUDE.md').write_text(content, encoding='utf-8')
            self._respond(200, {'ok': True})
        except Exception as e:
            self._respond(500, {'error': str(e)})

    def _respond(self, code, data):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(body))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        pass  # silencia logs

if __name__ == '__main__':
    import socketserver
    with socketserver.TCPServer(('', PORT), Handler) as httpd:
        print(f'personalcanvas -> http://localhost:{PORT}')
        httpd.serve_forever()
