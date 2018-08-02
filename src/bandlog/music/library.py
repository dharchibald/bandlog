# Yields a list chunk of size n from list
def group(list, n):
  for i in range(0, len(list), n):
    yield list[i:i+n]
