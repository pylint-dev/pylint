"""Warnings for using open() with an invalid mode string."""

__revision__ = 0

open('foo.bar', 'w', 2)
open('foo.bar', 'rw')
open(name='foo.bar', buffering=10, mode='rw')
open(mode='rw', name='foo.bar')
open('foo.bar', 'U+')
open('foo.bar', 'rb+')
open('foo.bar', 'Uw')
open('foo.bar', 2)
open('foo.bar', buffering=2)
WRITE_MODE = 'w'
open('foo.bar', 'U' + WRITE_MODE + 'z')
