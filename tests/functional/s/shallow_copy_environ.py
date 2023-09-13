"""Tests for shallow-copy-environ"""
# pylint: disable=wrong-import-position, reimported, ungrouped-imports, import-error, wrong-import-order

import copy
import os

copy.copy(os.environ)  # [shallow-copy-environ]

# Copying a dictionary is okay
test_dict = {}
copy.copy(test_dict)

# Test with renaming the functions
from copy import copy as test_cp
import os as o

test_cp(o.environ)  # [shallow-copy-environ]

# Regression test for non inferable objects
import copy
from missing_library import MissingObject

copy.copy(MissingObject)

# Deepcopy is okay
import copy
import os

copy.deepcopy(os.environ)

# Edge cases
copy.copy()  # [no-value-for-parameter]
copy.copy(x=test_dict)
copy.copy(x=os.environ)  # [shallow-copy-environ]
copy.copy(**{"x": os.environ})  # [shallow-copy-environ]
copy.copy(**{"y": os.environ})  # [unexpected-keyword-arg]
copy.copy(y=os.environ)  # [no-value-for-parameter, unexpected-keyword-arg]
