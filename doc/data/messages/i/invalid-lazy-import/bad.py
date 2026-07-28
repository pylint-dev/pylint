try:
    lazy import json  # [invalid-lazy-import]
except ImportError:
    json = None
