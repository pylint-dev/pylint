"""
	Pylint score:  -6
"""
import os

import nonexistent


def loop():
	count = 0
	for i in range(5):
		count += 1
	print(count)

path =   '/tmp'
os.path.exists(path)
