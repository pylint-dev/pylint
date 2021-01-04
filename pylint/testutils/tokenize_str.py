# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import tokenize
from io import StringIO


def _tokenize_str(code):
    return list(tokenize.generate_tokens(StringIO(code).readline))
