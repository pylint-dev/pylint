import threading

with threading.Lock():  # [useless-with-lock]
    print("Make your bed.")
with threading.Lock():  # [useless-with-lock]
    print("Sleep in it")
