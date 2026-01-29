#!/usr/bin/env bash
set -euo pipefail

# Prevent Python from writing __pycache__/ bytecode files into the repo.
export PYTHONDONTWRITEBYTECODE=1

cd "$(dirname "$0")/.."
python3 -m unittest discover -s tests -v
