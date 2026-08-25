#!/bin/sh
cd "$(dirname "$0")"
lsof -ti :8080 | xargs kill 2>/dev/null
nohup python3 -m http.server 8080 >/tmp/notes-server.log 2>&1 &
disown
sleep 0.3
open http://localhost:8080
