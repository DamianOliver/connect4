import math

def calc(num_paths, depth):
    for i in range(depth):
        if i < 5:
            print(i, 0)
        else:
            print(i, ((num_paths * math.factorial(i)) / (25 * 24 * 23 * 22 * 21)) * 100)

calc(12, 25)