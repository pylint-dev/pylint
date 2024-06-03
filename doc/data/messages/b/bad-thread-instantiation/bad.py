import threading


def thread_target(n):
    print(n**2)


thread = threading.Thread(lambda: None)  # [bad-thread-instantiation]
thread.start()
