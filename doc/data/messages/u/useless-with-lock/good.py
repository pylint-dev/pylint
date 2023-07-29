import threading

lock = threading.Lock()
with lock:
    print("Make your bed.")
with lock:
    print("Sleep in it.")
