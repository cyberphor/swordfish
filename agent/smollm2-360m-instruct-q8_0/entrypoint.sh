#!/bin/sh

set -e
uvicorn swordfish.main:api --host 0.0.0.0 --port 8181
