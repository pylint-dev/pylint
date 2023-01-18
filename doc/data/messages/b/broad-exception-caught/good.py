try:
    import platform_specific_module
except ImportError:
    platform_specific_module = None

try:
    1 / 0
except ZeroDivisionError:
    pass
