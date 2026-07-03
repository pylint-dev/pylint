# Agent guidelines

## AST-based checking

Pylint is an AST-based linter built on [astroid](https://github.com/pylint-dev/astroid).
When writing or modifying checkers, prefer **`isinstance` against concrete astroid node
types** combined with domain knowledge of Python syntax, rather than duck-typing with
`getattr`/`hasattr`.

The visitor pattern from `BaseChecker` already narrows the node type for you: a
`visit_call` method only receives `nodes.Call`, a `visit_assign` only receives
`nodes.Assign`, and so on. Inside such a method, the node's structure is known — its
attributes follow from the grammar (e.g. a `nodes.Call` always has `.func` and `.args`).
Walk and type-check that known structure with `isinstance` instead of probing for
attributes defensively.

Good:

```python
def visit_call(self, node: nodes.Call) -> None:
    if isinstance(node.func, nodes.Attribute):
        ...
```

Avoid:

```python
def visit_call(self, node) -> None:
    if hasattr(node.func, "attrname"):  # don't probe — check the type
        ...
```

This keeps checks precise, readable, and aligned with astroid's typed node API.

### Caveat: astroid proxies and `Uninferable`

`isinstance` checks the _static_ node type. Some astroid objects — `bases.Instance`,
`Generator`, `BoundMethod`/`UnboundMethod`, and `util.Uninferable` — resolve attributes
through `__getattr__`, proxying to a wrapped node. So `hasattr(obj, "x")` can be True at
runtime on an object whose class has no `x`, and a naive `isinstance(obj, ConcreteNode)`
will _drop_ cases the old `hasattr` caught (e.g. an exception inferred to an `Instance`
that proxies `ancestors`, or an `AsyncGenerator` that proxies `locals`).

When replacing such a guard:

- Include the proxy base in the type tuple — e.g. `(nodes.ClassDef, bases.Instance)`, or
  `(nodes.LocalsDictNodeNG, bases.Proxy)` for anything exposing `qname`.
- If the check is a behavioral _capability_ spanning heterogeneous nodes with no common
  base — or the proxied node may legitimately lack the attribute (a `BoundMethod` can
  wrap a `Lambda`, which has no `.decorators`) — keep `hasattr`. That is honest
  duck-typing, not a grammar check, and `isinstance` cannot express it safely.
