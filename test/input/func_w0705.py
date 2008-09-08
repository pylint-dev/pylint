"""test misordered except 
"""

__revision__ = 1

try:
    __revision__ += 1
except Exception:
    __revision__ = None
except TypeError:
    __revision__ = None

try:
    __revision__ += 1
except LookupError:
    __revision__ = None
except IndexError:
    __revision__ = None

try:
    __revision__ += 1
except (LookupError, NameError):
    __revision__ = None
except (IndexError, UnboundLocalError):
    __revision__ = None

try:
    __revision__ += 1
except:
    pass
except Exception:
    pass

try:
    __revision__ += 1
except TypeError:
    __revision__ = None
except:
    __revision__ = None 

try:
    __revision__ += 1
except Exception:
    pass
except:
    pass
