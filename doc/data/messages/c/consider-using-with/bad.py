file = open("apple.txt", "r", encoding="utf8")  # [consider-using-with]
contents = file.read()
file.close()

worst = open("banana.txt", "r", encoding="utf8").read()  # [consider-using-with]
