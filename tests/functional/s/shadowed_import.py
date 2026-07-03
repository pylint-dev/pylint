# pylint: disable=missing-docstring,unused-import,import-error, consider-using-from-import
# pylint: disable=wrong-import-order

from pathlib import Path
from some_other_lib import CustomPath as Path   # [shadowed-import]

from pathlib import Path  # [reimported]
import FastAPI.Path as Path  # [shadowed-import]

from pandas._libs import algos
import pandas.core.algorithms as algos  # [shadowed-import]

from sklearn._libs import second as libalgos
import sklearn.core.algorithms as second

import Hello
from goodbye import CustomHello as Hello   # [shadowed-import]
