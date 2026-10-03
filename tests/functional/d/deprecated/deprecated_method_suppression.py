"""Test that versions below Py3.10 will not emit useless-suppression for
disabling deprecated-method (on a method deprecated in Py3.10.

This test can be run on all Python versions, but it will lack value when
Pylint drops support for 3.9."""
# pylint: disable=import-error, unused-import

import threading.current_thread  # pylint: disable=deprecated-method
