#!/usr/bin/env python3
"""
Lightweight Python server for the Interview Prep Tracker.
No dependencies beyond the standard library.
"""

import http.server
import json
import os
import socketserver

PORT = int(os.environ.get("PORT", 3000))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
DATA_FILE = os.path.join(BASE_DIR, "progress.json")


def get_progress():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def save_progress(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PUBLIC_DIR, **kwargs)

    def do_GET(self):
        if self.path == "/api/progress":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(get_progress()).encode())
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/api/progress":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length))
            pid = body.get("problemId")
            user = body.get("user")
            solved = body.get("solved", False)

            if pid and user:
                progress = get_progress()
                if pid not in progress:
                    progress[pid] = {}
                progress[pid][user] = solved
                save_progress(progress)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Quieter logging
        pass


def get_local_ip():
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "localhost"


if __name__ == "__main__":
    local_ip = get_local_ip()
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        print(f"\n{'='*50}")
        print(f"🎯 Interview Prep Tracker is LIVE!")
        print(f"{'='*50}")
        print(f"\n   Local:   http://localhost:{PORT}")
        print(f"   Network: http://{local_ip}:{PORT}")
        print(f"\n   Share the Network URL with Yash! 🚀")
        print(f"   Press Ctrl+C to stop.\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server stopped.")
