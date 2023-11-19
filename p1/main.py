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
                for j in range(0, int(pow(p, 2))):
                    y = y + 1                           # (4)
                p = p + 1         

    return y               


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
        return [get_input_by_index(n, i, case) for i in range(n)]
    elif case == WORST_CASE:
        return [get_input_by_index(n, i, case) for i in range(n)]


def get_input_by_index(n: int, i: int, case: int) -> int:
    case0 = 0
    case1 = 0
    case2 = 0

    for j in range(i, n):
        k = n
        while k > 0:                            
            k = floor(k/3)
            case0 = case0 + 1   

    for m in range(i, n):                        
        for l in range(m, n):
            for t in range(n, 0, -1):
                for z in range(n, 0, -t):
                    case1 = case1 + 1

    p = 0
    while p < n:
        for j in range(0, int(pow(p, 2))):
            case2 = case2 + 1                       
        p = p + 1  
    
    if case == BEST_CASE:
        signif = min(case0, case1, case2)
    elif case == WORST_CASE:
        signif = max(case0, case1, case2)
    
    if signif == case0:
        return 0
    elif signif == case1:
        return 1
    elif signif == case2:
        return 2
        
def get_case(case: int) -> str:
    if case == BEST_CASE:
        return "Best Case"
    elif case == WORST_CASE:
        return "Worst Case"
    elif case == AVERAGE_CASE:
        return "Average Case"
    else:
        return "Unknown Case"

if __name__ == "__main__":
    input_sizes = [1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
    cases = [BEST_CASE, WORST_CASE, AVERAGE_CASE]

    for input_size in input_sizes:
        for case in cases:
            if case == AVERAGE_CASE:
                elapsed_times = []
                for i in range(0, 10):
                    elapsed_times.append(call(input_size, case))
                print(f"Input size: {input_size}, Case: {get_case(case)}, Elapsed Time: {sum(elapsed_times)/len(elapsed_times):.5f}")
                continue
            print(f"Input size: {input_size}, Case: {get_case(case)}, Elapsed Time: {call(input_size, case):.5f}")

