#!/usr/bin/env sh

set -e

./llama-server --host 0.0.0.0 --port 8080 --jinja -m gemma-3-1b-pt-q4_0.gguf -n 512
