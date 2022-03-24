def test(param):
    if param:
        assertion_string = "There is an AssertionError"
    else:
        assertion_string = ""

    assert assertion_string
