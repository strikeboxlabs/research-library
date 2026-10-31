#!/usr/bin/env python3
"""Portable controller tests; no Docker daemon or API key is used."""
from pathlib import Path
import unittest

if __name__ == "__main__":
    tests = unittest.defaultTestLoader.discover(str(Path(__file__).parent / "tests"))
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    raise SystemExit(not result.wasSuccessful())
