"""Tests for the useless-with-lock message"""
# pylint: disable=missing-docstring
import threading
from threading import Lock, RLock, Condition, Semaphore, BoundedSemaphore


with threading.Lock():  # [useless-with-lock]
    ...

with Lock():  # [useless-with-lock]
    ...

with threading.Lock() as THIS_SHOULDNT_MATTER:  # [useless-with-lock]
    ...

with threading.RLock():  # [useless-with-lock]
    ...

with RLock():  # [useless-with-lock]
    ...

with threading.Condition():  # [useless-with-lock]
    ...

with Condition():  # [useless-with-lock]
    ...

with threading.Semaphore():  # [useless-with-lock]
    ...

with Semaphore():  # [useless-with-lock]
    ...

with threading.BoundedSemaphore():  # [useless-with-lock]
    ...

with BoundedSemaphore():  # [useless-with-lock]
    ...

LOCK = threading.Lock()
with LOCK:  # this is ok
    ...

RLOCK = threading.RLock()
with RLOCK:  # this is ok
    ...

COND = threading.Condition()
with COND:  # this is ok
    ...

SEM = threading.Semaphore()
with SEM:  # this is ok
    ...

B_SEM = threading.BoundedSemaphore()
with B_SEM:  # this is ok
    ...
