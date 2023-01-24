"""Regression test for https://github.com/PyCQA/pylint/issues/8018"""
# pylint: disable=expression-not-assigned, pointless-statement

import numpy as np
from scipy.fft import rfft


arr = np.array([[1, 2, 3], [4, 5, 6]])

arr[:, 0:2]
arr[:, True]
arr[:, "1"]  # [invalid-slice-index]

rfft(arr)[:, 0:2]
rfft(arr)[..., 0]
rfft(arr)[1, 0:]
rfft(arr)[1, None]
rfft(arr)[1, True]
rfft(arr)[False, 0]

arr_fft = rfft(arr)
arr_fft[:, 0:2]


rfft(arr)[:, "1"]  # [invalid-slice-index]
rfft(arr)[:, "1":]  # [invalid-slice-index]
rfft(arr)[:, "1":"2"]   # [invalid-slice-index, invalid-slice-index]
