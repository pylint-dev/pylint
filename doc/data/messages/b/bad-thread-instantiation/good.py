import threading


def thread_target(n):
    print(n**2)


thread = threading.Thread(target=thread_target, args=(10,))
thread.start()
