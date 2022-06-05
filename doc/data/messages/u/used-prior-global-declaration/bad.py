TOMATO = "black cherry"


def update_tomato():
    print(TOMATO)  # [used-prior-global-declaration]
    global TOMATO
    TOMATO = "cherry tomato"
