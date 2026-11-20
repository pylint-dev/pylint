"""``import pkg.sub`` is used when ``sub`` is reached through another name bound to ``pkg``.

https://github.com/pylint-dev/pylint/issues/8501
"""
# pylint: disable=import-error, import-outside-toplevel, missing-function-docstring
# pylint: disable=wrong-import-position, wrong-import-order, reimported, no-name-in-module
# pylint: disable=no-member, multiple-imports

# The case from the issue: the submodule is reached through an alias of its package.
import xml as _x
import xml.dom

_: _x.dom.Node

# Several levels.
import pkg_a as _a
import pkg_a.sub.leaf

_a.sub.leaf.run()

# An alias of an intermediate package.
import pkg_b.sub as _b_sub
import pkg_b.sub.leaf

_b_sub.leaf.run()

# A ``from`` import binds the package under another name too.
from pkg_c import other, sub
import pkg_c.sub.leaf

sub.leaf.run()
other.run()

# The alias is used, but not to reach the submodule.
import pkg_d as _d
import pkg_d.sub  # [unused-import]

_d.run()

# The alias reaches another submodule with the same last name.
import pkg_e as _e
import pkg_e.sub.leaf  # [unused-import]

_e.other.leaf.run()

# The alias belongs to another package that has an attribute with the same name.
import pkg_f as _f
import pkg_g.sub  # [unused-import]

_f.sub.run()

# The aliased import already imports the submodule, so the second import is redundant.
import pkg_h.sub as _h_sub
import pkg_h.sub  # [unused-import]

_h_sub.run()

# A relative import is not resolved.
from . import pkg_i
import pkg_j.pkg_i.leaf  # [unused-import]

pkg_i.leaf.run()

# A plain import is not affected.
import pkg_o  # [unused-import]

# The alias is used without any attribute.
import pkg_k as _k
import pkg_k.sub  # [unused-import]

print(_k)


def submodule_reached_inside_function():
    import pkg_l as _l
    import pkg_l.sub

    return _l.sub.run()


def submodule_not_reached_inside_function():
    import pkg_m as _m
    import pkg_m.sub  # [unused-import]

    return _m.other.sub


def alias_shadowed_inside_function():
    import pkg_n as _n
    import pkg_n.sub  # [unused-import]

    print(_n)
    _n = object()
    return _n.sub


def several_names_in_one_import_inside_function():
    import pkg_p.sub, pkg_q  # [unused-import, unused-import]
