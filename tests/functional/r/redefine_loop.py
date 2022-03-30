"""Test case for variable redefined in inner loop."""
for item in range(0, 5):
    print("hello")
    for item in range(5, 10): #[redefined-loop-name]
        print(item)
        print("yay")
    print(item)
    print("done")
