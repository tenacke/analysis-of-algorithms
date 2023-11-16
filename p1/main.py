from math import *
from random import *
from time import *

BEST_CASE = 0
WORST_CASE = 1
AVERAGE_CASE = 2

def function(arr: list) -> int:
    y = 0
    n = len(arr)
    for i in range(0, n):
        if arr[i] == 0:                                 # (1)
            for j in range(i, n): 
                y = y + 1                               # (2)
                k = n
                while k > 0:                            # (3)
                    k = floor(k/3)
                    y = y + 1                           # (4)
        elif arr[i] == 1:
            for m in range(i, n):
                y = y + 1                               # (2)
                for l in range(m, n):
                    for t in range(n, 0, -1):
                        for z in range(n, 0, -t):
                            y = y + 1                   # (4)
        else:
            y = y + 1                                   # (3)
            p = 0
            while p < n:
                for j in range(0, pow(p, 2)):
                    y = y + 1                           # (4)
                p = p + 1                        


def call(n: int, case: int) -> int:
    arr = get_input(n, case)
    initial_time = time()
    function(arr)
    final_time = time()
    return final_time - initial_time



def get_input(n: int, case: int):
    if case == AVERAGE_CASE:
        return [randint(0, 2) for i in range(n)]
    elif case == BEST_CASE:
        pass
    elif case == WORST_CASE:
        pass


if __name__ == "__main__":
    input_sizes = [1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
    cases = [BEST_CASE, WORST_CASE, AVERAGE_CASE]

    for input_size in input_sizes:
        for case in cases:
            print(f"Input size: {input_size}, Case: {case}, Elapsed Time: {call(input_size)}")

