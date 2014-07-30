"""Warnings for using open() with an invalid mode string."""

open('foo.bar', 'w', 2)
open('foo.bar', 'rw')  # [bad-open-mode]
open(name='foo.bar', buffering=10, mode='rw')  # [bad-open-mode]
open(mode='rw', name='foo.bar')  # [bad-open-mode]
open('foo.bar', 'U+')  # [bad-open-mode]
open('foo.bar', 'rb+')  # [bad-open-mode]
open('foo.bar', 'Uw')  # [bad-open-mode]
open('foo.bar', 2)
open('foo.bar', buffering=2)
WRITE_MODE = 'w'
open('foo.bar', 'U' + WRITE_MODE + 'z')  # [bad-open-mode]
