#!/usr/bin/env python3
import http.server
import socketserver

class NoCacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

PORT = 5000
Handler = NoCacheHTTPRequestHandler

with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    print(f"Serving at http://0.0.0.0:{PORT}/")
    print("Cache-Control headers enabled - browsers will not cache files")
    print(f"LLM Instructions: http://0.0.0.0:{PORT}/llm-instructions.html")
    print(f"LLM Instructions JSON: http://0.0.0.0:{PORT}/llm-instructions.json")
    httpd.serve_forever()
