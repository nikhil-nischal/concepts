#!/usr/bin/env python3
"""Static file server plus a POST /api/save endpoint so index.html's
in-page editor can write markdown edits back to disk. Local use only."""
import http.server
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/api/save":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))
        target = os.path.realpath(os.path.join(ROOT, body["path"].lstrip("/")))
        if not target.startswith(ROOT + os.sep) or not target.endswith(".md"):
            self.send_error(400, "invalid path")
            return
        with open(target, "w", encoding="utf-8") as f:
            f.write(body["content"])
        self.send_response(200)
        self.end_headers()


if __name__ == "__main__":
    http.server.test(HandlerClass=Handler, port=8080)
