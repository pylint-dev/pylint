"""Warnings for using open() with an invalid mode string."""

open('foo.bar', 'w', 2)
open('foo.bar', 'rw')  # [bad-open-mode]
open(name='foo.bar', buffering=10, mode='rw')  # [bad-open-mode]
open(mode='rw', name='foo.bar')  # [bad-open-mode]
open('foo.bar', 'U+')
open('foo.bar', 'rb+')
open('foo.bar', 'Uw')  # [bad-open-mode]
open('foo.bar', 2)  # [bad-open-mode]
open('foo.bar', buffering=2)
WRITE_MODE = 'w'
open('foo.bar', 'U' + WRITE_MODE + 'z')  # [bad-open-mode]
open('foo.bar', 'br')  # [bad-open-mode]
open('foo.bar', 'wU')  # [bad-open-mode]
open('foo.bar', 'r+b')
open('foo.bar', 'r+')
open('foo.bar', 'w+')
open('foo.bar', 'xb')  # [bad-open-mode]
