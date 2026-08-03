# Materialize the iterator into a collection so it can be reused
gen = (x for x in range(3))
data = list(gen)
for i in range(2):
    for item in data:
        print(item)
