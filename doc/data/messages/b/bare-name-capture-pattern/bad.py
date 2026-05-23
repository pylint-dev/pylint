red = 0
green = 1
blue = 2


def func(color):
    match color:
        case red:  # [bare-name-capture-pattern]
            print("I see red!")
        case green:  # [bare-name-capture-pattern]
            print("Grass is green")
        case blue:
            print("I'm feeling the blues :(")
