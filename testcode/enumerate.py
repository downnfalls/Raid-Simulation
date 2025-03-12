a = ["Geeks", "for", "Geeks"]

# Iterating list using enumerate to get both index and element
for i, name in enumerate(a):
    print(f"Index {i}: {name}")

# Converting to a list of tuples
print(list(enumerate(a)))

# Index 0: Geeks
# Index 1: for
# Index 2: Geeks
# [(0, 'Geeks'), (1, 'for'), (2, 'Geeks')]