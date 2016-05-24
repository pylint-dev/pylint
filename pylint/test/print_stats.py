from __future__ import print_function

import os
from glob import glob

from pstats_print2list import get_pstats_print2list, print_pstats_list

fname_pattern = os.path.expanduser(
    os.environ.get('PYLINT_STATS', '~/pylint.stats'))
fnames = glob(fname_pattern)
cum_list = get_pstats_print2list(
    fnames, sort='cumulative',
    filter_fnames=['pylint/checkers', 'pylint/extensions'],
    limit=25, exclude_fnames=['test', '__init__.py'])
call_list = get_pstats_print2list(
    fnames, sort='calls',
    filter_fnames=['pylint/checkers', 'pylint/extensions'],
    limit=25, exclude_fnames=['test', '__init__.py'])
print("Cumulative")
print_pstats_list(cum_list)
print("Calls")
print_pstats_list(call_list)
