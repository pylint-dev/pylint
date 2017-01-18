# Copyright (c) 2016 Dropbox, Inc.
"""Makes pylint not complain about unused imports if they are used in type annotations."""

from __future__ import (
    absolute_import,
    division,
    print_function,
)

import re
import tokenize

import astroid
from astroid.node_classes import NodeNG
from astroid.context import InferenceContext

from pylint.checkers import BaseChecker
from pylint.interfaces import IRawChecker
from pylint.lint import PyLinter

# Note: This module is in astroid.brain but astroid sticks it in the root.
from brain_namedtuple_enum import infer_named_tuple

MYPY = False
if MYPY:
    from typing import Optional, Iterator, Callable, List

TYPING_SUBSCRIPTABLE_CLASSES = {
    # These are types that have metaclasses with __getitem__ methods
    # that return new classes of the base class.
    'typing.Generic',
    'typing.Tuple',
    'typing.Callable',
    # Older versions of typing have this as classes.
    'typing.Union',
    'typing.Optional',
}

TYPING_SUBSCRIPTABLE_INSTANCES = {
    # Newer versions of the typing module say Union = _Union(..)
    'typing._Union',
    'typing._Optional',
}

def infer_typing_subscript(node, context=None):
    # type: (NodeNG, Optional[InferenceContext]) -> Iterator[NodeNG]
    """Return the inference for things like Generic[T], etc."""
    assert isinstance(node, astroid.Subscript)
    for value in node.value.infer(context=context):
        if isinstance(value, astroid.ClassDef):
            for cls in TYPING_SUBSCRIPTABLE_CLASSES:
                if value.is_subtype_of(cls):
                    return iter([value])
        if isinstance(value, astroid.Instance):
            if value.qname() in TYPING_SUBSCRIPTABLE_INSTANCES:
                # Now infer the value to get the ClassDef
                return iter(value.inferred())

    raise astroid.UseInferenceDefault

def infer_typing_call(node, context=None):
    # type: (NodeNG, Optional[InferenceContext]) -> Iterator[NodeNG]
    """Infer the type for certain special cases in the typing module."""
    assert isinstance(node, astroid.Call)
    for inferred in node.func.infer():
        if inferred.qname() == 'typing.NamedTuple':
            # This is essentially a namedtuple with different arguments
            # so we fix the args up and infer a named tuple.
            fields = node.args[1]
            old, fields.elts = fields.elts, [i.elts[0] for i in fields.elts]
            ret = infer_named_tuple(node, context)
            # Don't forget to put the elts back afterward because this may be called multiple times.
            fields.elts = old
            return ret
        if inferred.qname() == 'typing.NewType':
            # NewType(X, Y) is pretty much Y.
            return node.args[1].infer(context=context)
        if inferred.qname() == 'typing.TypeVar':
            # TypeVar('T2') returns a TypeVar class.
            return iter([inferred])
    raise astroid.UseInferenceDefault

def call_looks_like(*names):
    # type: (*str) -> Callable[[astroid.Call], bool]
    """Return a function that will tell you if a Call object has a particular name."""
    s_names = set(names)

    def _looks_like(node):
        # type: (astroid.Call) -> bool
        """Return whether a Call object has a particular name."""
        func = node.func
        if isinstance(func, astroid.Attribute):
            return func.attrname in s_names
        if isinstance(func, astroid.Name):
            return func.name in s_names
        return False
    return _looks_like

def build_assign(value, line_num):
    # type: (str, int) -> NodeNG
    """Create an Assign object that can be added to the module.

    Also fixes the line_numbers and the module so context can be shown.
    """
    ret = astroid.parse('_ = {}'.format(value)).body[0]

    def _fix_tree(tree):
        tree.fromlineno = tree.tolineno = tree.lineno = int(line_num)
        for k in tree.get_children():
            _fix_tree(k)

    _fix_tree(ret)
    return ret

TYPE_ANNOTATION = re.compile(r'#\s*type:\s*(.*)')  # # type:
IGNORE = re.compile(r'\s*ignore\b')
FUNCTION_ANNOTATION = re.compile(r'(\(.*\))\s*->\s*(.*)')
STAR_ARGS = re.compile(r'([(,]\s*)\*{1,2}')  # "(*Any" or "... , *Any" or "... , **Any" or
EMPTY_ARGS = re.compile(r'\(\s*\)')  # ( any-whitespace )
UNTYPED_ELLIPSIS_ARGS = re.compile(r'\(\s*\.{3}\s*\)')  # ( any-whitespace ... any-whitespace )

def expr_for_comment(comment):
    # type: (str) -> Optional[str]
    """Return a compilable string to represent a type annotation."""

    # Skip if the comment does not start with '# type:'.
    m = TYPE_ANNOTATION.match(comment)
    if not m:
        return None
    expr = m.group(1)  # Everything after '# type:'

    # Skip if it's "# type: ignore"
    if IGNORE.match(expr):
        return None

    # Does it look like a signature annotation?
    m = FUNCTION_ANNOTATION.match(expr)
    if m:
        arg_types, return_type = m.groups()
        if EMPTY_ARGS.match(arg_types) or UNTYPED_ELLIPSIS_ARGS.match(expr):
            # `...` is not valid Python 2 syntax, so just return the return_type.
            expr = return_type
        else:
            # Remove the parens and any *, ** from the arguments.
            arg_types = STAR_ARGS.sub(r'\1', arg_types)[1:-1]
            expr = '%s, %s' % (arg_types, return_type)

    # Skip if expr can't be parsed using compile().
    try:
        compile(expr, '<string>', 'eval')
    except Exception:
        return None

    return expr

def find_insert_point(node, lineno):
    # type: (NodeNG, int) -> int
    """Find the insertion point for the lineno"""
    for i, child in enumerate(node.body):
        if child.tolineno >= lineno:
            # This child node is past the line so insert here.
            return i

def fill_scope_map(scope_map, node):
    # type: (List[NodeNG], NodeNG) -> None
    """Fill in the scope_map so that we get a quick lookup table of line numbers to scopes."""
    if not isinstance(node, (astroid.Module, astroid.ClassDef, astroid.FunctionDef)):
        return

    # We want our line numbers to be 1 indexed, however fromlineno and to lineno
    # are 0 indexed so add 1, except fromlineno always starts one line after the
    # def or class so just don't add 1 to that one.
    for line in range(node.fromlineno, node.tolineno + 1):
        scope_map[line] = node

    for child in node.get_children():
        fill_scope_map(scope_map, child)

def inject_imports(module):
    # type: (NodeNG) -> NodeNG
    assert isinstance(module, astroid.Module)

    if not module.pure_python:
        return module

    stream = module.stream()
    if not stream:
        return module

    # Don't bother checking files without annotations.
    encoding = module.file_encoding or 'utf-8'
    if not re.search(r'#\s*type:', stream.read().decode(encoding)):
        return module

    # Build a scope_map for faster lookups.
    scope_map = [module] * (module.tolineno + 1)
    fill_scope_map(scope_map, module)

    # Tokenize the file looking for those juicy # type: annotations.
    stream.seek(0)
    module.injected_lines = []
    tokens = tokenize.generate_tokens(lambda: stream.readline().decode(encoding))
    for tok_type, tok_val, (lineno, _), _, _ in tokens:
        if tok_type == tokenize.COMMENT:
            expr = expr_for_comment(tok_val)
            if expr:
                # Now convert that expression to an Assign node and insert it in the module.
                assign = build_assign(expr, lineno)
                scope = scope_map[lineno]
                i = find_insert_point(scope, lineno)
                if isinstance(scope.body[i], astroid.Pass) and len(scope.body) == 1:
                    # If what we have is a single pass statement then replace it with the assign.
                    # This is to avoid 'unnecessary-pass' warnings.
                    scope.body[i] = assign
                else:
                    scope.body.insert(i, assign)
                assign.parent = scope
                module.injected_lines.append(lineno)

    return module


class IgnoreMyPyWarnings(BaseChecker):
    """Checker that disables certain events on the added lines.

    Note: Creating a checker was the only way I found to do this.

    'multiple-statements': The way we add expressions to assignments will cause multiple
    statements on the same line so that's the only way to fix it.

    """
    __implements__ = IRawChecker

    name = 'ignore-mypy'
    msgs = {
        # Apparently you have to define something so that this runs.
        'W9999': ('Unused',
                  'ignore-mypy-errors',
                  'Used to disable mypy errors on added lines'),
    }

    def process_module(self, module):
        # type: (NodeNG) -> None
        for line in getattr(module, 'injected_lines', []):
            self.linter.disable('multiple-statements', scope='module', line=line)


def register(linter):
    # type: (PyLinter) -> None
    linter.register_checker(IgnoreMyPyWarnings(linter))

astroid.MANAGER.register_transform(astroid.Module, inject_imports)
astroid.MANAGER.register_transform(astroid.Subscript, astroid.inference_tip(infer_typing_subscript))
astroid.MANAGER.register_transform(astroid.Call, astroid.inference_tip(infer_typing_call),
                                   call_looks_like('NamedTuple', 'NewType', 'TypeVar'))
