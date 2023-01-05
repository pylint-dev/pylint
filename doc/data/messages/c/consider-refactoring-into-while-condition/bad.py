a = [1,2,3,4,5]

while True:  # [consider-refactoring-into-while-condition]
  if len(a) == 0:
    break
  a.pop()
