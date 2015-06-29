"""test misordered except
"""

__revision__ = 1

try:
    __revision__ += 1
except Exception:
    __revision__ = 0
except TypeError:
    __revision__ = 0

try:
    __revision__ += 1
except LookupError:
    __revision__ = 0
except IndexError:
    __revision__ = 0

try:
    __revision__ += 1
except (LookupError, NameError):
    __revision__ = 0
except (IndexError, UnboundLocalError):
    __revision__ = 0

try:
    __revision__ += 1
except:
    pass
except Exception:
    pass

try:
    __revision__ += 1
except TypeError:
    __revision__ = 0
except:
    __revision__ = 0

try:
    __revision__ += 1
except Exception:
    pass
except:
    pass
