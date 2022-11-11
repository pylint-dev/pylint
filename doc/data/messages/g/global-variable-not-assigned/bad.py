TOMATO = "black cherry"


def update_tomato():
    global TOMATO  # [global-variable-not-assigned]
    print(TOMATO)
