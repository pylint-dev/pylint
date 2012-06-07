"""Test for W0623, overwriting names in exception handlers."""

__revision__ = ''

def new_style():
    """Some exceptions can be unpacked."""
    try:
        pass
    except IOError as (errno, message): # this is fine
        print errno, message
    except IOError as (new_style, tuple): # W0623 twice
        print new_style, tuple
        
