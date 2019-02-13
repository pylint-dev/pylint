""" Testing string format with a failed inference. This should not crash. """
# pylint: disable=using-constant-test
import collections
"{dict[0]}".format(dict=collections.defaultdict(int))

COMMENT = "message %s %s %s" % (0, *(1 if "cond" else 2,) * 2)
