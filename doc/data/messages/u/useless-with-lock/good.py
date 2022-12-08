import threading

lock = threading.Lock()
with lock:
    print("This is good!")
