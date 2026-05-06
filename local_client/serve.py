"""
Tiny local HTTP server for index.html.

Why not just open index.html directly?
  Browsers treat file:// pages as "null" origin and block all outgoing
  fetch() calls (CORS policy). Serving over http://localhost fixes this.

Usage:
  python3 serve.py           # serves on port 8080 and opens the browser
  python3 serve.py 3000      # optional: custom port
"""

import http.server
import socketserver
import webbrowser
import os
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080

os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # suppress request logs for a cleaner terminal


socketserver.TCPServer.allow_reuse_address = True

print(f"Serving at  http://localhost:{PORT}")
print("Press Ctrl+C to stop.\n")
webbrowser.open(f"http://localhost:{PORT}")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
