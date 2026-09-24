"""Regression test: ``no-value-for-parameter`` must not fire when a required
argument is supplied via ``**`` unpacking of a dict whose contents pylint
cannot statically prove.

The patterns below were all observed as fresh false positives in ansible,
sentry and home-assistant when running the proposed implementation from
https://github.com/pylint-dev/pylint/pull/11002 against open-source code.
They share a single shape: a callable with required parameters is invoked
with ``**something``, and ``something`` is populated dynamically (forwarded
``**kwargs``, ``dict.update``, ``setdefault``, a loop, constant-keyed
assignment, or an opaque external source). None of these calls should
emit ``no-value-for-parameter``.

Each FP block is paired with a sibling call that exposes a genuinely
missing required argument (direct kwarg or literal ``**{...}`` covering
only a subset of the parameters). Those siblings must still emit
``no-value-for-parameter`` so the gate is not over-suppressing.
"""
# pylint: disable=missing-docstring,too-few-public-methods,unused-argument

from dataclasses import dataclass
from typing import Any


@dataclass
class Point:
    x: int
    y: int


def needs_two(a: int, b: int) -> int:
    return a + b


# 1. Outer ``**kwargs`` parameter forwarded to a callee with required params.
#    This is the dominant pattern -- any thin wrapper / facade does this.
def forward_to_ctor(**kwargs: Any) -> Point:
    return Point(**kwargs)


def forward_to_func(**kwargs: Any) -> int:
    return needs_two(**kwargs)


class Forwarder:
    def relay(self, **kwargs: Any) -> int:
        return needs_two(**kwargs)


# Paired violation: a direct call missing ``y`` is still caught.
Point(x=1)  # [no-value-for-parameter]


# 2. Dict populated via ``dict.update`` before being unpacked
#    (``data_kwargs.update({...})`` then ``Klass(**data_kwargs)`` --
#    sentry slack entrypoint).
def via_update() -> Point:
    data = {"x": 1}
    data.update({"y": 2})
    return Point(**data)


# Paired violation: a literal ``**{"x": ...}`` missing ``y`` is still caught.
Point(**{"x": 1})  # [no-value-for-parameter]


# 3. Dict populated via ``setdefault`` before being unpacked
#    (``update_snuba_query(..., **updated_query_fields)`` -- sentry
#    incidents/logic.py).
def via_setdefault() -> Point:
    data: dict[str, int] = {}
    data.setdefault("x", 0)
    data.setdefault("y", 0)
    return Point(**data)


# Paired violation: a literal ``**{"y": ...}`` missing ``x`` is still caught.
Point(**{"y": 0})  # [no-value-for-parameter]


# 4. Dict populated in a loop before being unpacked
#    (``NextDnsData(**coordinators)`` -- home-assistant nextdns).
PAIRS = [("x", 1), ("y", 2)]


def via_loop() -> Point:
    data: dict[str, int] = {}
    for name, value in PAIRS:
        data[name] = value
    return Point(**data)


# Paired violation: a literal ``**{"x": ...}`` whose loop counterpart would
# also stop short is still caught.
Point(**{"x": 2})  # [no-value-for-parameter]


# 5. Dict populated by constant-keyed assignment whose key string equals the
#    target parameter name (``kwargs[ATTR_MESSAGE] = message`` then
#    ``self.async_send_message(**kwargs)`` -- home-assistant notify/legacy).
ATTR_X = "x"
ATTR_Y = "y"


def via_constant_keys(value_x: int, value_y: int) -> Point:
    data: dict[str, int] = {}
    data[ATTR_X] = value_x
    data[ATTR_Y] = value_y
    return Point(**data)


# Paired violation: a literal ``**{ATTR_X: ...}`` missing ``y`` is still
# caught (the key resolves to ``"x"`` via inference).
Point(**{ATTR_X: 1})  # [no-value-for-parameter]


# 6. Dict obtained from an opaque external source then unpacked, optionally
#    after popping unrelated keys (``GalaxyAPI(self.galaxy, name,
#    **server_options)`` where ``server_options`` comes from
#    ``config.get_plugin_options(...)`` -- ansible galaxy CLI; same shape as
#    ``BigtableKVStorage(**options)`` in sentry).
def opaque_options() -> dict[str, Any]:
    return {"x": 1, "y": 2, "ignored": "ignored"}


def via_opaque_dict() -> Point:
    options = opaque_options()
    options.pop("ignored")
    # False positive unrelated to #8785: astroid does not model ``pop()``.
    return Point(**options)  # [unexpected-keyword-arg]


# Paired violation: a direct call to ``needs_two`` missing ``b`` is still
# caught.
needs_two(a=1)  # [no-value-for-parameter]


# 7. A dict literal is only trusted when every key is visible to pylint.
OTHER = {"b": 2}


def literal_with_known_unpack() -> int:
    return needs_two(**{"a": 1, **OTHER})


def literal_with_opaque_unpack(other: dict[str, int]) -> int:
    return needs_two(**{"a": 1, **other})


def literal_with_variable_key(key: str) -> int:
    return needs_two(**{"a": 1, key: 2})


def dict_comprehension(keys: list[str]) -> int:
    return needs_two(**{key: 1 for key in keys})


def literal_and_opaque(extra: dict[str, int]) -> int:
    return needs_two(**{"a": 1}, **extra)


def literal_and_forwarded(**kwargs: Any) -> int:
    return needs_two(**{"a": 1}, **kwargs)


def literal_and_unused_kwargs(**kwargs: Any) -> int:
    return needs_two(**{"a": 1})  # [no-value-for-parameter]
