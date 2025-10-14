#!/bin/sh

set -e

echo "[+] Starting the Swordfish backend..."
uvicorn swordfish.main:api --host 0.0.0.0 --port 8001
