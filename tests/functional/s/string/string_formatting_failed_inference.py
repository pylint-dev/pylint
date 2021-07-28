""" Testing string format with a failed inference. This should not crash. """
# pylint: disable=using-constant-test
import collections
"{dict[0]}".format(dict=collections.defaultdict(int))
