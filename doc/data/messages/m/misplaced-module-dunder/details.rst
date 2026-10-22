Only a dunder assigned a literal value is reported. A value that refers to a
name, such as ``__version__ = importlib.metadata.version("package")``, may
depend on an import and cannot be moved above it.

Dunders assigned inside an ``if`` or ``try`` block are not checked.
