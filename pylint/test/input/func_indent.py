# pylint: disable=print-statement
"""docstring"""
from __future__ import print_function

def totoo():
 """docstring"""
 print('malindented')

def tutuu():
    """docstring"""
    print('good indentation')

def titii():
     """also malindented"""
     1  # and this.

def tataa(kdict):
    """blank line unindented"""
    for key in ['1', '2', '3']:
        key = key.lower()

        if kdict.has_key(key):
            del kdict[key]

