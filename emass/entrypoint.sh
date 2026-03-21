#!/bin/sh

set -e
prism mock eMASSRestOpenApi.yaml --host 0.0.0.0 --port 4010
