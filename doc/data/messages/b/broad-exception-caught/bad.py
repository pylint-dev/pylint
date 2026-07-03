try:
    import platform_specific_module
except Exception:  # [broad-exception-caught]
    platform_specific_module = None
