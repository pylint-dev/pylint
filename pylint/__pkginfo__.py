# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE

from pkg_resources import DistributionNotFound, get_distribution

try:
    __version__ = get_distribution("pylint").version
except DistributionNotFound:
    __version__ = "2.8.2+"

# Kept for compatibility reason, see https://github.com/PyCQA/pylint/issues/4399
numversion = tuple(__version__.split("."))
