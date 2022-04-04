"""No message is emitted for variables overwritten in inner loops by default.
See redefined-loop-name optional checker."""
for item in range(0, 5):
    print("hello")
    for item in range(5, 10):
        print(item)
        print("yay")
    print(item)
    print("done")
