def important_string_manipulation(x: str, y: str) -> None:
    if x == "":  # [use-implicit-booleaness-not-comparison-to-string]
        print("x is an empty string")

    if y != "":  # [use-implicit-booleaness-not-comparison-to-string]
        print("y is not an empty string")
