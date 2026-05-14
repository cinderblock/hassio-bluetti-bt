"""Ensure vendored dependencies in /config/deps/ are importable."""

import sys
import os

_deps_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'deps'))
if os.path.isdir(_deps_dir) and _deps_dir not in sys.path:
    sys.path.insert(0, _deps_dir)
