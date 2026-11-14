"""A relative import is not a reimport of a top-level module of the same name."""
# pylint: disable=unused-import,import-error,no-name-in-module
# pylint: disable=import-outside-toplevel,missing-function-docstring

import json
import re
import re as re1  # [reimported]

from . import json as my_json

from .json import ONE


def load():
    from . import json as local_json
    return local_json
