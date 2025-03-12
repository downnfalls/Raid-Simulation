def myfunc(a, b):
  return a + b

x = map(myfunc, ('apple', 'banana', 'cherry'), ('orange', 'lemon', 'pineapple'))

print(x) #address map

#convert the map into a list, for readability:
print(list(x)) # value in map