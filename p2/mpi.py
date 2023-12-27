# Emre Kilic 2021400015, Kristina Trajkovski 2020400384, Group 47

from mpi4py import MPI    
import sys
import os

def enhance(s): # even
    return s[0] + s + s[-1]

def reverse(s): # odd
    return s[::-1]

def chop(s): # even
    if len(s) < 2:
        return s
    return s[:-1]

def trim(s): # odd
    if len(s) < 3:
        return s
    return s[1:-1]

def split(s): # even
    mid = len(s) // 2 + len(s) % 2
    return s[:mid]

class Main:
    def __init__(self, tree):
        self.tree = tree

class Node:
    def __init__(self, num_cycles, wears, maintenance_limit):
        self.num_cycles = num_cycles
        self.wears = wears # per instruction
        self.maintenance_limit = maintenance_limit
        self.children = [] # int array
        self.wear = 0

    def add_child(self, child):
        self.children.append(child)
        self.children = sorted(self.children)

    def isroot(self):
        return self.parent == None

    def isleaf(self):
        return len(self.children) == 0

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        func = [enhance, reverse, chop, trim, split] # states
        num_procs = int(f.readline())
        num_cycles = int(f.readline())
        wears = [int(i) for i in f.readline().split()]
        maintenance_limit = int(f.readline())
        nodes = [Node(num_cycles, wears, maintenance_limit) for i in range(num_procs)] # remember to substract 1 when indexing
        leafs = [i for i in range(num_procs)]
        nodes[0].id = 0
        nodes[0].state = 5
        nodes[0].parent = None
        for i in range(num_procs-1): # add information to the initialized nodes
            line = f.readline().split()
            nodes[int(line[0])-1].id = int(line[0])-1
            nodes[int(line[0])-1].parent = int(line[1])-1
            nodes[int(line[1])-1].add_child(int(line[0])-1)
            nodes[int(line[0])-1].state = func.index(eval(line[2]))
            try:
                leafs.remove(int(line[1])-1)
            except:
                pass
        
        for leaf in leafs:
            nodes[leaf].input = f.readline().strip()

    comm = MPI.COMM_SELF.Spawn("python", args=['client.py'], maxprocs=num_procs) # create new parallel processes

    for i in range(num_procs):
        comm.send(nodes[i], dest=i) # send the processes their node information

    
    with open(sys.argv[2], "w") as f:
        big_data = []
        while True:
            probe = comm.iprobe(source=MPI.ANY_SOURCE)
            if probe:
                data = comm.recv(source=MPI.ANY_SOURCE)
                if data == "finito beybiiii": # node 1 has finished all of its cycles
                    break
                if type(data) != str: # maintenance log
                    big_data.append(data)
                else:
                    f.write(data+'\n') # finished product
        maintenance_data = [f"{maint[0]}-{maint[2]}-{maint[1]}" for maint in sorted(big_data)]
        f.write("\n".join(maintenance_data))