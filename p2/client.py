# Emre Kilic 2021400015, Kristina Trajkovski 2020400384, Group 47

from mpi4py import MPI
from mpi import *

comm = MPI.Comm.Get_parent()

rank = comm.Get_rank()
size = comm.Get_size()

node = comm.recv(source=0)

node.comm = MPI.COMM_WORLD

for cycle in range(node.num_cycles):

    # get children data
    product = ""
    if node.isleaf():
        product = node.input
    else:
        for child in node.children:
            product += node.comm.recv(source=child)
    
    last_wearfactor = 0

    # do work and wear down
    if node.state == 0: # enhance
        product = enhance(product)
        last_wearfactor = node.wears[0]
        node.wear += last_wearfactor
        node.state = 4
    elif node.state == 1: # reverse
        product = reverse(product)
        last_wearfactor = node.wears[1]
        node.wear += last_wearfactor
        node.state = 3
    elif node.state == 2: # chop
        product = chop(product)
        last_wearfactor = node.wears[2]
        node.wear += last_wearfactor
        node.state = 0
    elif node.state == 3: # trim
        product = trim(product)
        last_wearfactor = node.wears[3]
        node.wear += last_wearfactor
        node.state = 1
    elif node.state == 4: # split
        product = split(product)
        last_wearfactor = node.wears[4]
        node.wear += last_wearfactor
        node.state = 2

    if node.wear >= node.maintenance_limit: # maintenance
        cost = (node.wear - node.maintenance_limit + 1) * last_wearfactor
        node.wear = 0
        comm.send([node.id+1, cycle+1, cost], dest = 0, tag=1)

    if rank != 0: # send finished product to parent
        node.comm.send(product, dest=node.parent)
    else: # send finished product to controller
        comm.send(product, dest=0, tag=0)

if rank == 0: # break the master/messenger process
    comm.send("finito beybiiii", dest=0, tag=1)
