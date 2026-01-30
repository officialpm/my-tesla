"""Repo-local Python runtime tweaks.

Python automatically imports `sitecustomize` (if present on sys.path) after the
standard `site` module.

We use this to keep the repo clean when running ad-hoc commands like:
  python3 -m unittest discover -s tests -v

Without this, Python can create `__pycache__/` and `*.pyc` files throughout the
repo, which are annoying and easy to accidentally commit.

This file contains no secrets and has no external side effects.
"""

import sys

# Keep the repo clean: never write bytecode caches into the working tree.
sys.dont_write_bytecode = True
