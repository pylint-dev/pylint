import unittest
from importlib.machinery import SourceFileLoader, SourcelessFileLoader

SourceFileLoader('unittest', unittest.__file__).exec_module()
