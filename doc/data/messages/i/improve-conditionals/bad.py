def func(expr, node_cls):
    # +1:[improve-conditionals]
    if not isinstance(expr, node_cls) or expr.attrname != "__init__":
        ...
