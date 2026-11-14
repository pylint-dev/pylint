"""Regression test for https://github.com/pylint-dev/pylint/issues/10193.

Shadowing the base module with an alias and calling a method named
``format`` on the alias used to emit a false ``no-name-in-module``.
"""
import fruits.basket as fruits

fruits.format()
