red = 0
green = 1
blue = 2


color = blue
match color:
    case red:  # [unreachable-match-patterns]
        print("I see red!")
    case green:  # [unreachable-match-patterns]
        print("Grass is green")
    case blue:
        print("I'm feeling the blues :(")
