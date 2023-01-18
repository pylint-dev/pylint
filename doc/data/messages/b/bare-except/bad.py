try:
    import platform_specific_module
except:  # [bare-except]
    platform_specific_module = None


try:
    1 / 0
except:  # [bare-except]
    pass
