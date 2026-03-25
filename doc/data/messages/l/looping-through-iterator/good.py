# 1. Define the iterator inside the loop so it restarts
for i in range(2):
    gen = (x for x in range(3))
    for item in gen:
        print(item)

# 2. Materialize the iterator into a collection
gen = (x for x in range(3))
data = list(gen)
for i in range(2):
    for item in data:
        print(item)

# 3. range objects are re-iterable and safe
range_obj = range(3)
for i in range(2):
    for item in range_obj:
        print(item)
