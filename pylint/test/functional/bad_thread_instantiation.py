# pylint: disable=missing-docstring
import threading


threading.Thread(lambda: None).run()  # [bad-thread-instantiation]
threading.Thread(group=None, target=lambda: None).run()
threading.Thread()
