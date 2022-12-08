import threading


with threading.Lock():  # [useless-with-lock]
    print("doesn't have the effect you think it has...")
