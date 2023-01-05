"""Test for cython pure python cython.declare"""
import cython

MY_VAR = cython.declare(cython.int, 0)
