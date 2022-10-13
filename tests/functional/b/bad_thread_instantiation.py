# pylint: disable=missing-docstring, redundant-keyword-arg
import threading


threading.Thread(lambda: None).run()  # [bad-thread-instantiation]
threading.Thread(None, lambda: None)  # [bad-thread-instantiation]
threading.Thread(lambda: None, group=None)  # [bad-thread-instantiation]
threading.Thread()  # [bad-thread-instantiation]

threading.Thread(group=None, target=lambda: None).run()
