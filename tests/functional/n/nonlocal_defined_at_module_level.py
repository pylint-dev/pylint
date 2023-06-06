"""Test ``nonlocal`` defined at module-level"""


nonlocal APPLE  # [nonlocal-defined-at-module-level]
APPLE = 42
