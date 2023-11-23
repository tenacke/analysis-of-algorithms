from math import *
from random import *
from time import *

BEST_CASE = 0
WORST_CASE = 1
AVERAGE_CASE = 2

BESTS = {}
WORSTS = {}

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
        return BESTS[n]
    elif case == WORST_CASE:
        return WORSTS[n]

def set_input_by_index(n: int, i: int) -> int:
    case0 = 0
    case1 = 0
    case2 = 0

    case0 = (n-i)*floor(log(n, 3)+1)
    case1 = int(sum([ceil(n/t) for t in range(1, n+1)])*(((n*(n+1)+i*(i-1))/2)-i*n))
    case2 = int(n*(n-1)*(2*n-1)/6)

    best = min(case0, case1, case2)
    worst = max(case0, case1, case2)
    
    if best == case0:
        BESTS[n].append(0)
    elif best == case1:
        BESTS[n].append(1)
    elif best == case2:
        BESTS[n].append(2)
    
    if worst == case0:
        WORSTS[n].append(0)
    elif worst == case1:
        WORSTS[n].append(1)
    elif worst == case2:
        WORSTS[n].append(2)

def set_input_by_index2(n: int, i: int) -> int:
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
    
    best = min(case0, case1, case2)
    worst = max(case0, case1, case2)
    
    if best == case0:
        BESTS[n].append(0)
    elif best == case1:
        BESTS[n].append(1)
    elif best == case2:
        BESTS[n].append(2)
    
    if worst == case0:
        WORSTS[n].append(0)
    elif worst == case1:
        WORSTS[n].append(1)
    elif worst == case2:
        WORSTS[n].append(2)
        
def get_case(case: int) -> str:
    if case == BEST_CASE:
        return "best"
    elif case == WORST_CASE:
        return "worst"
    elif case == AVERAGE_CASE:
        return "average"

if __name__ == "__main__":
    input_sizes = [1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
    cases = [BEST_CASE, WORST_CASE, AVERAGE_CASE]

    for n in input_sizes:
        BESTS[n] = []
        WORSTS[n] = []
        for i in range(0, n):
            set_input_by_index(n, i)

    for input_size in input_sizes:
        for case in cases:
            if case == AVERAGE_CASE:
                elapsed_times = []
                for i in range(0, 10):
                    elapsed_time = call(input_size, case)
                    elapsed_times.append(elapsed_time)
                    print(f"Case: {get_case(case)} Size: {input_size} Elapsed Time (s): {elapsed_time:.7f}")
                print(f"Case: {get_case(case)} Size: {input_size} Elapsed Time (s): {sum(elapsed_times)/len(elapsed_times):.7f}")
                continue
            print(f"Case: {get_case(case)} Size: {input_size} Elapsed Time (s): {call(input_size, case):.7f}")

