file = open("foo.txt", "r", encoding="utf8")  # [consider-using-with]
contents = file.read()
file.close()
