"""https://github.com/PyCQA/pylint/issues/5370"""

try:
    pass
except ImportError as err:
    try:
        pass
    except ImportError as err:  # [redefined-outer-name]
        pass
    print(err)

try:
    pass
except ImportError as err:
    try:
        pass
    except ImportError as err2:
        pass
    print(err)

try:
    try:
        pass
    except ImportError as err:
        pass
except ImportError:
    try:
        pass
    except ImportError as err:
        pass
    print(err)


try:
    try:
        pass
    except ImportError as err:
        pass
except ImportError as err:
    try:
        pass
    except ImportError:
        pass
    print(err)

try:
    pass
except ImportError as err:
    try:
        pass
    except ImportError as err2:
        try:
            pass
        except ImportError as err:  # [redefined-outer-name]
            pass
    print(err)
