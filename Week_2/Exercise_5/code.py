import sys
x = sum([int(arg) for arg in sys.argv[1:]]) / len(sys.argv[1:])
print(f"{x} Pass" if x > 5 else f"{x} Fail")
