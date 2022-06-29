x = ["a" "b"]  # [implicit-str-concat]

with open("hello.txt" "r") as f:  # [implicit-str-concat]
    print(f.read())
