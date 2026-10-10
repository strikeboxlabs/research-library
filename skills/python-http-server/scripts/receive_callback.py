"""Receive one bounded, explicitly controlled HTTP POST body; no file serving."""
import argparse
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bind', required=True)
    parser.add_argument('--port', required=True, type=int)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--max-bytes', type=int, default=65536)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535 or not 1 <= args.max_bytes <= 1048576:
        parser.error('port/size outside supported range')
    if args.output.exists() or not args.output.parent.is_dir():
        parser.error('output must be fresh in an existing private directory')

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            if self.path != '/evidence':
                self.send_error(404); return
            if self.headers.get('Transfer-Encoding'):
                self.send_error(400, 'chunked transfer unsupported'); return
            try:
                length = int(self.headers.get('Content-Length', ''))
            except ValueError:
                self.send_error(411); return
            if not 1 <= length <= args.max_bytes:
                self.send_error(413); return
            self.connection.settimeout(5)
            try:
                body = self.rfile.read(length)
            except TimeoutError:
                self.send_error(408); return
            if len(body) != length:
                self.send_error(400, 'incomplete body'); return
            try:
                with args.output.open('xb') as stream:
                    stream.write(body)
            except FileExistsError:
                self.send_error(409); return
            self.send_response(201); self.send_header('Content-Length', '0'); self.end_headers()
            print(f'{datetime.now(timezone.utc).isoformat()} POST /evidence bytes={length}', flush=True)

    with HTTPServer((args.bind, args.port), Handler) as server:
        print(f'Listening on {args.bind}:{args.port}; stop after selected evidence arrives', flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    main()
