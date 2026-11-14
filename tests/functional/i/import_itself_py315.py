"""Test module lazily importing itself (PEP 810)."""
lazy from . import import_itself_py315  # [import-self]

print(import_itself_py315)
