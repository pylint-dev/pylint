"""Testing Pylint with the socket module

Pylint Problem
==============

Version used:

    - Pylint 0.10.0
    - Logilab common 0.15.0
    - Logilab astng 0.15.1

False E1101 positive, line 23:

    Instance of '_socketobject' has no 'connect' member

"""
__revision__ = None

import socket

if __name__ == "__main__":

    SCKT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SCKT.connect(('127.0.0.1', 80))
    SCKT.close()
