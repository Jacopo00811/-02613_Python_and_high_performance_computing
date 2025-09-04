import sys
x = filter(lambda x: x%2 == 0, [int(arg) for arg in sys.argv[1:]])
print(list(x))
