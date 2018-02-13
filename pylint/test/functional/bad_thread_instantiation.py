# pylint: disable=missing-docstring
import threading


threading.Thread(lambda: None).run()  # [bad-thread-instantiation]
threading.Thread(None, lambda: None)
threading.Thread(group=None, target=lambda: None).run()
threading.Thread() # [bad-thread-instantiation]
